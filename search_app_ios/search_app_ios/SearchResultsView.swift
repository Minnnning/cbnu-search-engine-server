import SwiftUI

struct SearchResult: Identifiable {
    let id: String
    let site: String
    let title: String
    let url: String
    let contentPreview: String? // content의 일부를 저장
}

struct ApiResponse: Decodable {
    struct Hits: Decodable {
        struct InnerHits: Decodable {
            struct Source: Decodable {
                let site: String
                let title: String
                let url: String
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

    var body: some View {
        ZStack {
            Color.appBackgroundColor
                .ignoresSafeArea()
            
            VStack {
                if isLoading {
                    ProgressView("Loading...")
                } else if let errorMessage = errorMessage {
                    Text("Error: \(errorMessage)").foregroundColor(.red)
                } else if results.isEmpty {
                    Text("No results found")
                } else {
                    List(results) { result in
                        VStack(alignment: .leading) {
                            Text(result.site)
                                .font(.headline)
                            
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
            }
            .onAppear(perform: fetchSearchResults)
            .navigationTitle("검색 결과")
        }
    }

    func fetchSearchResults() {
        guard let url = URL(string: "http://1.248.115.71:9334/search") else {
            errorMessage = "Invalid URL"
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
                        // 옵셔널 체이닝과 nil 병합 연산자를 사용해 안전하게 언래핑
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

