import SwiftUI

struct SearchResult: Identifiable {
    let id: String
    let site: String
    let title: String
    let url: String
    let date: String
    let contentPreview: String? // content의 일부를 저장
}

struct ApiResponse: Decodable {
    struct Hits: Decodable {
        struct InnerHits: Decodable {
            struct Source: Decodable {
                let site: String
                let title: String
                let url: String
                let date: String
                let content: String?
            }

            let _id: String
            let _source: Source
        }

        let hits: [InnerHits]
    }

    let hits: Hits
}

struct SearchApiResponse: Decodable {
    let tokens: [String]
    let results: ApiResponse // `results`가 전체 검색 결과를 포함
}

struct SearchResultsView: View {
    var searchQuery: String
    @State private var results: [SearchResult] = []
    @State private var isLoading: Bool = false
    @State private var errorMessage: String? = nil

    // DateFormatter를 사용하여 날짜만 출력하는 포맷을 지정
    private let inputDateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd HH:mm:ss" // 서버에서 받은 날짜 형식
        return formatter
    }()
    
    private let outputDateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd" // 원하는 출력 형식
        return formatter
    }()

    var body: some View {
        ZStack {
            // 배경 색 설정
            Color.appBackgroundColor
                .ignoresSafeArea()

            if isLoading {
                ProgressView("Loading...")
            } else if let errorMessage = errorMessage {
                Text("Error: \(errorMessage)")
                    .foregroundColor(.red)
            } else if results.isEmpty {
                Text("No results found")
            } else {
                // ZStack 안에 List를 추가하여 배경색이 적용되도록 설정
                List {
                    ForEach(results) { result in
                        VStack(alignment: .leading) {
                            HStack {
                                Text(result.site)
                                    .font(.headline)
                                
                                // 날짜 표시 (시간 없이)
                                Text(result.date)
                                    .font(.caption)
                                    .foregroundColor(.gray)
                            }

                            // 제목 클릭시 링크로 이동
                            Link(destination: URL(string: result.url)!) {
                                Text(result.title)
                                    .font(.subheadline)
                                    .foregroundColor(.blue)
                            }

                            if let contentPreview = result.contentPreview {
                                Text(contentPreview)
                                    .font(.footnote)
                                    .foregroundColor(.gray)
                                    .lineLimit(2) // Only show two lines of content
                            }
                        }
                    }
                }
                .scrollContentBackground(.hidden) // 리스트의 기본 배경 색상을 숨김
            }
        }
        .onAppear(perform: fetchSearchResults)
        .navigationTitle("검색 결과")
    }

    func fetchSearchResults() {
        // 'Info.plist'에서 URL 가져오기
        guard let urlString = Bundle.main.object(forInfoDictionaryKey: "API_SEARCH") as? String,
              let url = URL(string: urlString) else {
            errorMessage = "Info.plist에서 유효하지 않은 URL"
            isLoading = false
            return
        }

        // 검색 요청을 위한 HTTP POST 요청
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // 요청 바디 설정 (검색어 포함)
        let body: [String: Any] = ["query": searchQuery]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        
        isLoading = true
        errorMessage = nil
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                isLoading = false
                
                if let error = error {
                    errorMessage = "Failed to load data: \(error.localizedDescription)"
                    return
                }
                
                guard let data = data else {
                    errorMessage = "No data received"
                    return
                }
                
                do {
                    // FastAPI의 /search 엔드포인트에서 받은 응답을 파싱
                    let decodedResponse = try JSONDecoder().decode(SearchApiResponse.self, from: data)
                    self.results = decodedResponse.results.hits.hits.map { hit in
                        // 날짜 변환: 서버의 날짜 문자열을 사용해 `Date`로 변환 후 다시 `String`으로 변환
                        let dateString = hit._source.date
                        let date: String
                        
                        if let parsedDate = inputDateFormatter.date(from: dateString) {
                            date = outputDateFormatter.string(from: parsedDate)
                        } else {
                            date = "Invalid date"
                        }

                        // contentPreview 처리
                        let contentPreview = hit._source.content?.trimmingCharacters(in: .whitespacesAndNewlines)
                            .components(separatedBy: .newlines)
                            .joined(separator: " ")
                            .prefix(100)
                        
                        let previewText = contentPreview.map(String.init) ?? "" // 옵셔널 값 변환 및 처리
                        
                        return SearchResult(
                            id: hit._id,
                            site: hit._source.site,
                            title: hit._source.title,
                            url: hit._source.url,
                            date: date,
                            contentPreview: previewText.isEmpty ? nil : previewText
                        )
                    }
                } catch {
                    errorMessage = "Failed to parse data: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
}
