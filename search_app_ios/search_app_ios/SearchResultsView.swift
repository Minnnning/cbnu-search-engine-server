import SwiftUI

struct SearchResult: Identifiable, Equatable {
    let id: String
    let site: String
    let title: String
    let url: String
    let date: String
    let contentPreview: String?

    static func == (lhs: SearchResult, rhs: SearchResult) -> Bool {
        return lhs.id == rhs.id
    }
}


struct ApiResponse: Decodable {
    let id: String
    let site: String
    let title: String
    let url: String
    let date: String
    let contentPreview: String?
}


struct SearchApiResponse: Decodable {
    let query: String
    let results: [ApiResponse]
}

struct SearchResultsView: View {
    var searchQuery: String
    @State private var results: [SearchResult] = []
    @State private var isLoading: Bool = false
    @State private var errorMessage: String? = nil
    @State private var currentPage = 0
    @State private var hasMoreResults = true // 더 많은 결과가 있는지 여부

    private let pageSize = 10

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
            Color.appBackgroundColor
                .ignoresSafeArea()

            if isLoading && results.isEmpty {
                ProgressView("Loading...")
            } else if let errorMessage = errorMessage {
                Text("Error: \(errorMessage)")
                    .foregroundColor(.red)
            } else if results.isEmpty {
                Text("No results found")
            } else {
                List {
                    ForEach(results) { result in
                        VStack(alignment: .leading) {
                            HStack {
                                Text(result.site)
                                    .font(.headline)
                                
                                Text(result.date)
                                    .font(.caption)
                                    .foregroundColor(.gray)
                            }

                            // 제목 클릭 시 링크로 이동
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
                        .onAppear {
                            if result == results.last && hasMoreResults {
                                loadMoreResults()
                            }
                        }
                    }

                    if isLoading {
                        ProgressView()
                    }
                }
                .scrollContentBackground(.hidden)
            }
        }
        .onAppear(perform: fetchSearchResults)
        .navigationTitle("검색 결과")
    }

    func fetchSearchResults() {
        guard let urlString = Bundle.main.object(forInfoDictionaryKey: "API_SEARCH") as? String else {
            errorMessage = "Info.plist에서 유효하지 않은 URL"
            isLoading = false
            return
        }

        // page와 size를 URL 파라미터로 추가
        let urlWithParams = "\(urlString)?page=\(currentPage)&size=\(pageSize)"
        
        guard let url = URL(string: urlWithParams) else {
            errorMessage = "Invalid URL format"
            isLoading = false
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
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
                    let decodedResponse = try JSONDecoder().decode(SearchApiResponse.self, from: data)
                    
                    let newResults = decodedResponse.results.map { response in
                        let dateString = response.date
                        let date: String
                        if let parsedDate = inputDateFormatter.date(from: dateString) {
                            date = outputDateFormatter.string(from: parsedDate)
                        } else {
                            date = dateString
                        }

                        let contentPreview = response.contentPreview?.trimmingCharacters(in: .whitespacesAndNewlines)
                            .components(separatedBy: .newlines)
                            .joined(separator: " ")
                            .prefix(100)
                        
                        let previewText = contentPreview.map(String.init) ?? ""

                        return SearchResult(
                            id: response.id,
                            site: response.site,
                            title: response.title,
                            url: response.url,
                            date: date,
                            contentPreview: previewText.isEmpty ? nil : previewText
                        )
                    }
                    
                    if newResults.count < pageSize {
                        hasMoreResults = false
                    }
                    
                    results.append(contentsOf: newResults)
                    
                } catch {
                    errorMessage = "Failed to parse data: \(error.localizedDescription)"
                }
            }
        }.resume()
    }


    func loadMoreResults() {
        currentPage += 1
        fetchSearchResults()
    }
}
