// 필요한 모듈 및 라이브러리를 임포트합니다.
import dayjs from "dayjs"; // 날짜 처리를 위한 라이브러리
import { log } from "../common/log"; // 로그 기능을 제공하는 모듈
import noticeScripts from "./scripts/index"; // 스크립트 정보를 포함하는 모듈

// 스크래핑 관련 모듈 및 상수를 임포트합니다.
import { scraping } from "../scraper/scraper"; // 웹 스크래핑 기능
import { excludeNotices, excludeSites } from "./constant"; // 스크래핑 제외 대상

// 날짜 문자열을 ISO 형식으로 변환하는 함수
const getISODate = (date: string) => {
  const replacedDate = date.replace(/[년|일|월]/g, ".");
  return dayjs(replacedDate).toISOString();
};

// 재시도 관련 맵과 최대 재시도 횟수 설정
const retryScriptMap = new Map<string, number>();
const maxRetryCount = 2;

// 공지사항 스크래핑을 수행하는 비동기 함수
export const scrapingNotices = async () => {

  // 모든 공지 스크립트를 순회
  for (const noticeScript of noticeScripts) {
    // 제외 대상 사이트인지 확인
    if (excludeSites.some((site) => site.script.site_id === noticeScript.site_id)) {
      continue; // 제외 대상 사이트는 건너뜁니다.
    }

    let noticeList = [];
    try {
      // 공지사항 목록을 스크래핑합니다.
      noticeList = await scraping({
        scenario: {
          name: noticeScript.site,
          jsScript: noticeScript,
          scrapFunctionName: noticeScript.getNoticeList.name,
          url: noticeScript.url,
          waitSelector: noticeScript.noticeListSelector,
        },
      });
      if (!noticeList.length) {
        throw new Error("공지사항 목록을 가져올 수 없습니다");
      }
    } catch (error) {
      // 스크래핑 중 오류 처리
      console.error("[ERROR] 공지사항 목록 가져오기 - ", noticeScript, error);
      log(`[ERROR] 공지사항 목록 가져오기 - ${JSON.stringify({ error, noticeScript })}`);
      continue;
    }

    // 스크래핑된 각 공지사항에 대한 처리
    for (const notice of noticeList) {
      const retryCount = retryScriptMap.get(notice.url) ?? 0;

      if (retryCount >= maxRetryCount) {
        if (retryCount === maxRetryCount) {
          log(`[WARN] 스크립트 재실행 회수(${retryCount}) 초과 - ${JSON.stringify(notice)}`);
        }
        continue;
      }

      if (excludeNotices.some((excludeNotice) => excludeNotice.url === notice.url)) {
        continue; // 제외 대상 공지사항은 건너뜁니다.
      }

      const duplicateResponse = await ArticleApiService.articleControllerIsDuplicated({
        url: notice.url,
      });

      if (duplicateResponse.isDuplicated) continue; // 중복된 공지사항은 처리하지 않습니다.

      // 공지사항 내용을 스크래핑합니다.
      const content = await scraping({
        scenario: {
          name: noticeScript.site,
          jsScript: noticeScript,
          scrapFunctionName: noticeScript.getContentsHtml.name,
          url: notice.url,
          waitSelector: noticeScript.noticeContentsSelector,
        },
      }).catch((error) => {
        log(`[ERROR] 공지사항 등록 - ${JSON.stringify({ error, noticeScript })}`);
        const retryCount = retryScriptMap.get(notice.url) ?? 0;
        retryScriptMap.set(notice.url, retryCount + 1);
      });

      if (!!(noticeScript as any).getContentDate) {
        notice.date = await scraping({
          scenario: {
            name: noticeScript.site,
            jsScript: noticeScript,
            scrapFunctionName: (noticeScript as any).getContentDate.name,
            url: notice.url,
            waitSelector: noticeScript.noticeContentsSelector,
          },
        });
      }

      try {
        // 공지사항을 등록합니다.
        const result = await ArticleApiService.articleControllerCreate({
          requestBody: {
            boardId: notice.site_id,
            title: notice.title,
            url: notice.url,
            dateTime: getISODate(notice.date),
            content,
          },
        });

        if (result.success) {
          console.log("[INFO] 공지사항 등록 완료 - ", notice);
        }
      } catch (error) {
        const retryCount = retryScriptMap.get(notice.url) ?? 0;
        retryScriptMap.set(notice.url, retryCount + 1);
        log(`[ERROR] 공지사항 등록 - ${JSON.stringify({ contentLength: content.length, error, notice })}`);
        console.error("[ERROR] 공지사항 등록 - ", error, notice);
      }
    }
  }
};
