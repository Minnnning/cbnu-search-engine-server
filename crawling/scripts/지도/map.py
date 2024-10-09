import pymysql

from dotenv import load_dotenv
import os

# .env 파일을 로드하여 환경 변수로 설정
load_dotenv(dotenv_path='crawling/test.env')

hosturl =  os.getenv('DB_HOST')
username = os.getenv('DB_USER')
userpassword = os.getenv('DB_PASS')
dbname = os.getenv('DB_NAME1')

table_N = 'notice_board'

location = [
    {"title": "E1-1 사범대학실험동", "latitude": 36.628952, "longitude":127.460798, "site":"지도", "url":"https://maps.app.goo.gl/uGq6uG1dvK7Weyni9", "category":"정보", "date":"2024-10-07"},
    {"title": "E1-2 사범대학강의동", "latitude": 36.628592, "longitude":127.460299, "site":"지도", "url":"https://maps.app.goo.gl/QkXjLiZ31RcU6ney7", "category":"정보", "date":"2024-10-07"},
    {"title": "E2 개신문화관", "latitude": 36.628273, "longitude": 127.459367, "site":"지도", "url":"https://maps.app.goo.gl/UUfVqhtJfWFa5kHn6", "category":"정보", "date":"2024-10-07"},
    {"title": "E3 제1학생회관", "latitude": 36.627633, "longitude":127.458753, "site":"지도", "url":"https://maps.app.goo.gl/PUDoXfp9VB7fDuCE7", "category":"정보", "date":"2024-10-07"},
    {"title": "E3-1 NH관", "latitude": 36.627252, "longitude": 127.459346, "site":"지도", "url":"https://maps.app.goo.gl/jGwNAMp7YXAcnBqj9", "category":"정보", "date":"2024-10-07"},
    {"title": "E5 123학군단", "latitude": 36.627072, "longitude": 127.461791, "site":"지도", "url":"https://maps.app.goo.gl/wDQUN1zaxNsggjca6", "category":"정보", "date":"2024-10-07"},
    {"title": "E4-3 보조체육관", "latitude": 36.626881, "longitude": 127.462472, "site":"지도", "url":"https://maps.app.goo.gl/3XYbNNjgss28nGjr5", "category":"정보", "date":"2024-10-07"},
    {"title": "E4-2 운동장본부석", "latitude": 36.626530, "longitude": 127.462249, "site":"지도", "url":"https://maps.app.goo.gl/bgwAaKdnjp7VWV9X6", "category":"정보", "date":"2024-10-07"},
    {"title": "E4-1 CBNU스포츠센터", "latitude": 36.627303, "longitude": 127.460546, "site":"지도", "url":"https://maps.app.goo.gl/Rf4M2rEX4ocpU2dC9", "category":"정보", "date":"2024-10-07"},
    {"title": "E6 특고압 변전실", "latitude": 36.628060, "longitude": 127.462146, "site":"지도", "url":"https://maps.app.goo.gl/xdbWEw1kocqe15nD9", "category":"정보", "date":"2024-10-07"},
    {"title": "E7-1 의과대학1호관", "latitude": 36.624991, "longitude": 127.461081, "site":"지도", "url":"https://maps.app.goo.gl/KHPQjN148nzYrZFy7", "category":"정보", "date":"2024-10-07"},
    {"title": "E7-2 임상연구동", "latitude": 36.624976, "longitude": 127.460502, "site":"지도", "url":"https://maps.app.goo.gl/WaUprZSRNxXzm2VFA", "category":"정보", "date":"2024-10-07"},
    {"title": "E7-3 의과대학2호관", "latitude": 36.625569, "longitude": 127.460244, "site":"지도", "url":"https://maps.app.goo.gl/LTj5x9yWZsEpgo2Q7", "category":"정보", "date":"2024-10-07"},
    {"title": "E8-1 공과대학본관", "latitude": 36.626748, "longitude": 127.458259, "site":"지도", "url":"https://maps.app.goo.gl/WxokmNyrTupdcKSE8", "category":"정보", "date":"2024-10-07"},
    {"title": "E8-2 합동강의실", "latitude": 36.626362, "longitude": 127.457699, "site":"지도", "url":"https://maps.app.goo.gl/zPqYStnVxxnpe3mm7", "category":"정보", "date":"2024-10-07"},
    {"title": "E8-3 제2공학관", "latitude": 36.626124, "longitude": 127.458984, "site":"지도", "url":"https://maps.app.goo.gl/S52HhwTFRX3ZMjLV9", "category":"정보", "date":"2024-10-07"},
    {"title": "E8-4 제1공장동", "latitude": 36.625425, "longitude": 127.458989, "site":"지도", "url":"https://maps.app.goo.gl/7AKegFUfjSjWLg8g6", "category":"정보", "date":"2024-10-07"},
    {"title": "E8-5 제2공장동", "latitude": 36.625085, "longitude": 127.458872, "site":"지도", "url":"https://maps.app.goo.gl/c1zM46bwcNDvwe1K6", "category":"정보", "date":"2024-10-07"},
    {"title": "E8-6 제3공학관", "latitude": 36.624559, "longitude": 127.458498, "site":"지도", "url":"https://maps.app.goo.gl/4K6pJEehpNj5NvvF6", "category":"정보", "date":"2024-10-07"},
    {"title": "E8-7 전자정보1관", "latitude": 36.625423, "longitude": 127.458062, "site":"지도", "url":"https://maps.app.goo.gl/EngSNSYLdY9aA5nh6", "category":"정보", "date":"2024-10-07"},
    {"title": "E8-8 공학지원센터", "latitude": 36.624592, "longitude": 127.459236, "site":"지도", "url":"https://maps.app.goo.gl/241rsTdPSy95XSYWA", "category":"정보", "date":"2024-10-07"},
    {"title": "E8-9 신소재재료실험실", "latitude": 36.625172, "longitude": 127.459246, "site":"지도", "url":"https://maps.app.goo.gl/wgJ2V7frJwU2k8696", "category":"정보", "date":"2024-10-07"},
    {"title": "E8-10 제5공학관", "latitude": 36.624082, "longitude": 127.458088, "site":"지도", "url":"https://maps.app.goo.gl/i8mUTaUeu9fC2s3r9", "category":"정보", "date":"2024-10-07"},
    {"title": "E8-11 양진재(BTL)", "latitude": 36.624147, "longitude": 127.459569, "site":"지도", "url":"https://maps.app.goo.gl/YpdZGF7NXFGynNF78", "category":"정보", "date":"2024-10-07"},
    {"title": "E9 학연산공동기술연구원", "latitude": 36.625106, "longitude": 127.457191, "site":"지도", "url":"https://maps.app.goo.gl/sL7EUpJjtXymNtzR6", "category":"정보", "date":"2024-10-07"},
    {"title": "E10 전자정보2관", "latitude": 36.624876, "longitude": 127.457847, "site":"지도", "url":"https://maps.app.goo.gl/viBBwC6FSf1VR2f19", "category":"정보", "date":"2024-10-07"},
    {"title": "E11-1 목장창고", "latitude": 36.624076, "longitude": 127.457499, "site":"지도", "url":"https://maps.app.goo.gl/csPqWXjRsQTEPx3N9", "category":"정보", "date":"2024-10-07"},
    {"title": "E11-2 목장관리사", "latitude": 36.624187, "longitude": 127.457381, "site":"지도", "url":"https://maps.app.goo.gl/LJymyzjyXPjYosKL9", "category":"정보", "date":"2024-10-07"},
    {"title": "E11-3 우사", "latitude": 36.624008, "longitude": 127.457243, "site":"지도", "url":"https://maps.app.goo.gl/vvehHKDrLb6t54n38", "category":"정보", "date":"2024-10-07"},
    {"title": "E11-4 건조창고", "latitude": 36.624008, "longitude": 127.457259, "site":"지도", "url":"https://maps.app.goo.gl/XLrmyYLTiRbHFkQ99", "category":"정보", "date":"2024-10-07"},
    {"title": "E11-5 동물자원연구지원센터", "latitude": 36.623783, "longitude": 127.457012, "site":"지도", "url":"https://maps.app.goo.gl/UxW4KmjagaNbMAuP6", "category":"정보", "date":"2024-10-07"},
    {"title": "E12-1 수의과대학 및 동물병원", "latitude": 36.623241, "longitude": 127.456127, "site":"지도", "url":"https://maps.app.goo.gl/wJ2wYp4vNbsMydQo7", "category":"정보", "date":"2024-10-07"},
    {"title": "E12-2 수의과대학2호관", "latitude": 36.623478, "longitude": 127.456823, "site":"지도", "url":"https://maps.app.goo.gl/N9KC2xbmAN8S7q1J6", "category":"정보", "date":"2024-10-07"},
    {"title": "E12-3 실험동물연구지원센터", "latitude": 36.623802, "longitude": 127.456057, "site":"지도", "url":"https://maps.app.goo.gl/m8jtjaFaNsq8q4iZA", "category":"정보", "date":"2024-10-07"},

    {"title": "N2 법학전문대학원", "latitude": 36.631894, "longitude": 127.454450, "site":"지도", "url":"https://maps.app.goo.gl/iDUwsamTYa1utbfq8", "category":"정보", "date":"2024-10-07"},
    {"title": "N4 산학협력관", "latitude": 36.632501, "longitude": 127.455212, "site":"지도", "url":"https://maps.app.goo.gl/En7DasZiwVqwWgeg8", "category":"정보", "date":"2024-10-07"},
    {"title": "N5 국제교류본부 2호관", "latitude": 36.632082, "longitude": 127.455740, "site":"지도", "url":"https://maps.app.goo.gl/j1hQAaAEmMXW9Mhe9", "category":"정보", "date":"2024-10-07"},
    {"title": "N6 고시원", "latitude": 36.632484, "longitude": 127.455478, "site":"지도", "url":"https://maps.app.goo.gl/ub3hTZ1dVQ6PBFo4A", "category":"정보", "date":"2024-10-07"},
    {"title": "N7 형설관", "latitude": 36.632821, "longitude": 127.455891, "site":"지도", "url":"https://maps.app.goo.gl/rwFTvmjYFhbjr1bP6", "category":"정보", "date":"2024-10-07"},
    {"title": "N8 보육교사교육원(바이오프라이드고교학점제지원센터)", "latitude": 36.633068, "longitude": 127.456533, "site":"지도", "url":"https://maps.app.goo.gl/Jez8TBVdzgsCZmHc6", "category":"정보", "date":"2024-10-07"},
    {"title": "N9 국제교류본부 3호관", "latitude": 36.633266, "longitude": 127.457049, "site":"지도", "url":"https://maps.app.goo.gl/NDJc6hikSHjfLetA6", "category":"정보", "date":"2024-10-07"},
    {"title": "N10 대학본부,국제교류본부", "latitude": 36.630253, "longitude": 127.454716, "site":"지도", "url":"https://maps.app.goo.gl/ZJZVsvXiRGEyrmyY6", "category":"정보", "date":"2024-10-07"},
    {"title": "N11 공동실험실습관", "latitude": 36.629226, "longitude": 127.455439, "site":"지도", "url":"https://maps.app.goo.gl/qKu9AgedcBwVTydt9", "category":"정보", "date":"2024-10-07"},
    {"title": "N12 중앙도서관", "latitude": 36.628473, "longitude": 127.457442, "site":"지도", "url":"https://maps.app.goo.gl/b3eiyi37Fe76kTZYA", "category":"정보", "date":"2024-10-07"},
    {"title": "N13 경영학관", "latitude": 36.630076, "longitude": 127.456927, "site":"지도", "url":"https://maps.app.goo.gl/FpU7DXaeU2c74Crr7", "category":"정보", "date":"2024-10-07"},
    {"title": "N14 인문사회관(강의동)", "latitude": 36.630971, "longitude": 127.456463, "site":"지도", "url":"https://maps.app.goo.gl/PbazULhtPZ8pWyRc7", "category":"정보", "date":"2024-10-07"},
    {"title": "N15 사회과학대학", "latitude": 36.629723, "longitude": 127.457658, "site":"지도", "url":"https://maps.app.goo.gl/97RCX89tWLvyY32F8", "category":"정보", "date":"2024-10-07"},
    {"title": "N16-1 인문대학", "latitude": 36.630141, "longitude": 127.458631, "site":"지도", "url":"https://maps.app.goo.gl/AVCWvWZmPvW4bgm18", "category":"정보", "date":"2024-10-07"},
    {"title": "N16-2 미술관", "latitude": 36.630771, "longitude": 127.457247, "site":"지도", "url":"https://maps.app.goo.gl/5NwxMkw4bR4C2EgQ6", "category":"정보", "date":"2024-10-07"},
    {"title": "N16-3 미술과", "latitude": 36.630764, "longitude": 127.458523, "site":"지도", "url":"https://maps.app.goo.gl/7xgSxNHDXcSrEb3z8", "category":"정보", "date":"2024-10-07"},
    {"title": "N17-1 학생생활관본관(수위실)", "latitude": 36.631358, "longitude": 127.457506, "site":"지도", "url":"https://maps.app.goo.gl/ZbXbWLnNVt2zmuYk9", "category":"정보", "date":"2024-10-07"},
    {"title": "N17-2 학생생활관본관관리동", "latitude": 36.631515, "longitude": 127.457607, "site":"지도", "url":"https://maps.app.goo.gl/PpLqMzmoHwZkbe758", "category":"정보", "date":"2024-10-07"},
    {"title": "N17-3 개성재(진리관)", "latitude": 36.631012, "longitude": 127.457805, "site":"지도", "url":"https://maps.app.goo.gl/hpPuVpY5MCxvL7SN7", "category":"정보", "date":"2024-10-07"},
    {"title": "N17-4 개성재(정의관)", "latitude": 36.631198, "longitude": 127.458157, "site":"지도", "url":"https://maps.app.goo.gl/zwodejqgA4CiYaM89", "category":"정보", "date":"2024-10-07"},
    {"title": "N17-5 개성재(개척관)", "latitude": 36.631475, "longitude": 127.458348, "site":"지도", "url":"https://maps.app.goo.gl/zQquzogYpsoXBZQM7", "category":"정보", "date":"2024-10-07"},
    {"title": "N17-6 계영원", "latitude": 36.631899, "longitude": 127.458583, "site":"지도", "url":"https://maps.app.goo.gl/vnL5qzMFJkwYMozg8", "category":"정보", "date":"2024-10-07"},
    {"title": "N18 법학관", "latitude": 36.630963, "longitude": 127.459332, "site":"지도", "url":"https://maps.app.goo.gl/qgTQiyqYBPxMK4sp9", "category":"정보", "date":"2024-10-07"},
    {"title": "N19 제2본관", "latitude": 36.630574, "longitude": 127.459879, "site":"지도", "url":"https://maps.app.goo.gl/icZnXo9h4iBMtJJ9A", "category":"정보", "date":"2024-10-07"},
    {"title": "N20-1 생활과학대학", "latitude": 36.630394, "longitude": 127.460721, "site":"지도", "url":"https://maps.app.goo.gl/j7j9xBuoLjFF25dN6", "category":"정보", "date":"2024-10-07"},
    {"title": "N20-2 어린이집", "latitude": 36.630741, "longitude": 127.460342, "site":"지도", "url":"https://maps.app.goo.gl/9kd7HEcsNjAMTx95A", "category":"정보", "date":"2024-10-07"},
    {"title": "N21 은하수식당", "latitude": 36.629940, "longitude": 127.460227, "site":"지도", "url":"https://maps.app.goo.gl/FNmhGu7SWHNkGEvR7", "category":"정보", "date":"2024-10-07"},

    {"title": "S1-1 자연대1호관", "latitude": 36.627777, "longitude": 127.456699, "site":"지도", "url":"https://maps.app.goo.gl/Td1U2u2LPG1aSNhy9", "category":"정보", "date":"2024-10-07"},
    {"title": "S1-2 자연대2호관", "latitude": 36.627133, "longitude": 127.456899, "site":"지도", "url":"https://maps.app.goo.gl/zXguWr5vqQLJmMQk6", "category":"정보", "date":"2024-10-07"},
    {"title": "S1-3 자연대3호관", "latitude": 36.626676, "longitude": 127.456762, "site":"지도", "url":"https://maps.app.goo.gl/Nnr8Ks9zMEvfm9Wd9", "category":"정보", "date":"2024-10-07"},
    {"title": "S1-4 자연대4호관", "latitude": 36.626244, "longitude": 127.456630, "site":"지도", "url":"https://maps.app.goo.gl/CbcYGDwwwGogiRG38", "category":"정보", "date":"2024-10-07"},
    {"title": "S1-5 자연대5호관", "latitude": 36.625634, "longitude": 127.455839, "site":"지도", "url":"https://maps.app.goo.gl/xhfjy92AibVyuCfK7", "category":"정보", "date":"2024-10-07"},
    {"title": "S1-6 자연대6호관", "latitude": 36.625156, "longitude": 127.455997, "site":"지도", "url":"https://maps.app.goo.gl/E74sMfxZ8sZzWZX38", "category":"정보", "date":"2024-10-07"},
    {"title": "S1-7 과학기술도서관", "latitude": 36.626892, "longitude": 127.457034, "site":"지도", "url":"https://maps.app.goo.gl/6j764i3kh7Avm3az6", "category":"정보", "date":"2024-10-07"},
    {"title": "S2 정보화본부", "latitude": 36.626374, "longitude": 127.455466, "site":"지도", "url":"https://maps.app.goo.gl/is5y4HMp8CBA7fiv8", "category":"정보", "date":"2024-10-07"},
    {"title": "S3 본부관리동", "latitude": 36.626284, "longitude": 127.454468, "site":"지도", "url":"https://maps.app.goo.gl/jG2J5N7phFvcSf9LA", "category":"정보", "date":"2024-10-07"},
    {"title": "S4-1 전자정보3관", "latitude": 36.625621, "longitude": 127.454413, "site":"지도", "url":"https://maps.app.goo.gl/Cx7uSJPzLWVkpVGy6", "category":"정보", "date":"2024-10-07"},
    {"title": "S4-2 나이팅게일관", "latitude": 36.625262, "longitude": 127.454793, "site":"지도", "url":"https://maps.app.goo.gl/U7rFUajEJQXvL8rs7", "category":"정보", "date":"2024-10-07"},
    {"title": "S5-1 농장관리실", "latitude": 36.625121, "longitude": 127.453675, "site":"지도", "url":"https://maps.app.goo.gl/expdFRxqghEGe8h69", "category":"정보", "date":"2024-10-07"},
    {"title": "S5-2 농기계창고", "latitude": 36.624855, "longitude": 127.453675, "site":"지도", "url":"https://maps.app.goo.gl/JPDqeDreMLZ18Jc67", "category":"정보", "date":"2024-10-07"},
    {"title": "S6-1 자연대온실1", "latitude": 36.625213, "longitude": 127.453178, "site":"지도", "url":"https://maps.app.goo.gl/LBa2MuXHrjrdjRqE7", "category":"정보", "date":"2024-10-07"},
    {"title": "S7-1 에너지저장연구센터", "latitude": 36.625990, "longitude": 127.453753, "site":"지도", "url":"https://maps.app.goo.gl/oqXF65yubyZrPwdQA", "category":"정보", "date":"2024-10-07"},
    {"title": "S7-2 교육대학원,동아리방", "latitude": 36.626500, "longitude": 127.453625, "site":"지도", "url":"https://maps.app.goo.gl/QXbFftnSchosR3ib8", "category":"정보", "date":"2024-10-07"},
    {"title": "S8 야외공연장", "latitude": 36.626889, "longitude": 127.453917, "site":"지도", "url":"https://maps.app.goo.gl/wq1PB2xCLt6a6uzo9", "category":"정보", "date":"2024-10-07"},
    {"title": "S9 박물관", "latitude": 36.627698, "longitude": 127.455400, "site":"지도", "url":"https://maps.app.goo.gl/LRQ34scgpEGor8rt5", "category":"정보", "date":"2024-10-07"},
    {"title": "S13 목공실", "latitude": 36.628252, "longitude": 127.454520, "site":"지도", "url":"https://maps.app.goo.gl/3vTwQeJF5fgswrGN8", "category":"정보", "date":"2024-10-07"},
    {"title": "S14 제2학생회관", "latitude": 36.628006, "longitude": 127.454290, "site":"지도", "url":"https://maps.app.goo.gl/YJcN2NrkLqj6Mp6z6", "category":"정보", "date":"2024-10-07"},
    {"title": "S17-1 양성재(지선관)", "latitude": 36.627947, "longitude": 127.452323, "site":"지도", "url":"https://maps.app.goo.gl/13zgCfSeRVYR6Ef18", "category":"정보", "date":"2024-10-07"},
    {"title": "S17-2 양성재(명덕관)", "latitude": 36.627299, "longitude": 127.452743, "site":"지도", "url":"https://maps.app.goo.gl/yCWVsUDZ4bnMxL577", "category":"정보", "date":"2024-10-07"},
    {"title": "S17-3 양성재(신민관)", "latitude": 36.627225, "longitude": 127.452186, "site":"지도", "url":"https://maps.app.goo.gl/FoMy5om5twcd6aEB6", "category":"정보", "date":"2024-10-07"},
    {"title": "S17-4 v양현재(수위실)", "latitude": 36.627357, "longitude": 127.451269, "site":"지도", "url":"https://maps.app.goo.gl/uBr7PvgvVyS8GE1v7", "category":"정보", "date":"2024-10-07"},
    {"title": "S17-5 양현재(청운관)", "latitude": 36.627328, "longitude": 127.450476, "site":"지도", "url":"https://maps.app.goo.gl/XFTuQrjcQ6qKj8Ep7", "category":"정보", "date":"2024-10-07"},
    {"title": "S17-6 양현재(등용관)", "latitude": 36.627057, "longitude": 127.450971, "site":"지도", "url":"https://maps.app.goo.gl/E7pTU2Exchxd7cop8", "category":"정보", "date":"2024-10-07"},
    {"title": "S17-7 양현재(관리동)", "latitude": 36.627062, "longitude": 127.450287, "site":"지도", "url":"https://maps.app.goo.gl/X1nZr5vSwZND4bsf8", "category":"정보", "date":"2024-10-07"},
    {"title": "S18 승리관(운동부합숙소)", "latitude": 36.628505, "longitude": 127.451377, "site":"지도", "url":"https://maps.app.goo.gl/n1z3QgJKZdtfdmhG8", "category":"정보", "date":"2024-10-07"},
    {"title": "S19 종양연구소", "latitude": 36.628689, "longitude": 127.451749, "site":"지도", "url":"https://maps.app.goo.gl/ojxzNVBzSn9FJCgW6", "category":"정보", "date":"2024-10-07"},
    {"title": "S20 첨단바이오연구센터", "latitude": 36.628868, "longitude": 127.452373, "site":"지도", "url":"https://maps.app.goo.gl/PMzTXXAg6keBVSTx5", "category":"정보", "date":"2024-10-07"},
    {"title": "S21-3 농업과학기술교육센터", "latitude": 36.629515, "longitude": 127.451539, "site":"지도", "url":"https://maps.app.goo.gl/oxA62MRbmVK8kYc29", "category":"정보", "date":"2024-10-07"},
    {"title": "S21-4 농업생명환경대학", "latitude": 36.629460, "longitude": 127.452568, "site":"지도", "url":"https://maps.app.goo.gl/M4phYkEqm97DyhVT9", "category":"정보", "date":"2024-10-07"},
    {"title": "S21-5 농생대연구동", "latitude": 36.630125, "longitude": 127.453079, "site":"지도", "url":"https://maps.app.goo.gl/hGjqZZdftcNYBkwy8", "category":"정보", "date":"2024-10-07"},
    {"title": "S21-10 온실", "latitude": 36.630432, "longitude": 127.451561, "site":"지도", "url":"https://maps.app.goo.gl/axAJa9XHxErcBG7c6", "category":"정보", "date":"2024-10-07"},
    {"title": "S21-20 온실관리동", "latitude": 36.630618, "longitude": 127.451704, "site":"지도", "url":"https://maps.app.goo.gl/cryjNqjoU9LXmtZu7", "category":"정보", "date":"2024-10-07"},
    {"title": "S21-23 농기계실습실", "latitude": 36.630707, "longitude": 127.452361, "site":"지도", "url":"https://maps.app.goo.gl/i1NEEyg3rMvYYDoW7", "category":"정보", "date":"2024-10-07"},
    {"title": "S21-24 바이오시스템공학과", "latitude": 36.631040, "longitude": 127.451850, "site":"지도", "url":"https://maps.app.goo.gl/Ur8PnqVe8tm9qoew5", "category":"정보", "date":"2024-10-07"}
]

# MariaDB 연결
db_connection = pymysql.connect(host=hosturl, user=username, password=userpassword, db=dbname, charset='utf8')
cursor = db_connection.cursor()

if __name__ == "__main__":
    for loc in location:
        try:
            # 데이터베이스에 저장
            sql = f"INSERT INTO {table_N} (title, url, site,  latitude, longitude, category, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (loc['title'], loc['url'], loc['site'], loc["latitude"], loc["longitude"], loc["category"], loc["date"])
            cursor.execute(sql, values)
            db_connection.commit()
            print(f"Data inserted successfully: title={loc['title']}, site={loc['site']}")

        except pymysql.Error as e:
            print(f"Error {e.args[0]}, {e.args[1]}")
            db_connection.rollback()

    # WebDriver 및 DB 연결 닫기
    db_connection.close()
    print("map update completed.")
