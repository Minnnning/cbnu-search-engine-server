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

struct SearchResultsView: View {
    var searchQuery: String
    @State private var results: [SearchResult] = []
    @State private var isLoading: Bool = false
    @State private var errorMessage: String? = nil

    var body: some View {
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
                        
                        // Title as a clickable link
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
        .navigationTitle("Search Results")
    }

    func fetchSearchResults() {
        guard let url = URL(string: "http://elastic:dbr0vwg6lZHvuP_PqEo3@localhost:9200/notice_index/_search?q=title:\(searchQuery)") else {
            errorMessage = "Invalid URL"
            return
        }

        isLoading = true
        errorMessage = nil

        URLSession.shared.dataTask(with: url) { data, response, error in
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
                    let apiResponse = try JSONDecoder().decode(ApiResponse.self, from: data)
                    self.results = apiResponse.hits.hits.map { hit in
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

