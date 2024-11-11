// SearchResultsView
import SwiftUI
import MapKit

struct SearchResult: Identifiable, Equatable {
    let id: String
    let site: String
    let title: String
    let url: String
    let date: String
    let contentPreview: String?
    let latitude: Double?
    let longitude: Double?

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
    let latitude: Double?
    let longitude: Double?
}

struct SearchApiResponse: Decodable {
    let query: String
    let results: [ApiResponse]
}

struct MapPin: Identifiable {
    let id = UUID() // 각 핀에 고유 ID를 부여하기 위해 UUID 사용
    let coordinate: CLLocationCoordinate2D
}

struct SearchResultsView: View {
    var searchQuery: String
    @State private var results: [SearchResult] = []
    @State private var isLoading: Bool = false
    @State private var errorMessage: String? = nil
    @State private var currentPage = 0
    @State private var hasMoreResults = true
    @State private var selectedLocation: (latitude: Double, longitude: Double)? = nil
    @State private var showFullMap = false
    
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
                                    .lineLimit(2)
                            }
                            if let latitude = result.latitude, let longitude = result.longitude {
                                let pin = MapPin(coordinate: CLLocationCoordinate2D(latitude: latitude + 0.0002, longitude: longitude))
                                
                                Map(coordinateRegion: .constant(MKCoordinateRegion(
                                    center: CLLocationCoordinate2D(latitude: latitude, longitude: longitude),
                                    span: MKCoordinateSpan(latitudeDelta: 0.003, longitudeDelta: 0.003)
                                )), annotationItems: [pin]) { location in
                                    MapAnnotation(coordinate: location.coordinate) {
                                        Image(systemName: "mappin")
                                            .foregroundColor(.red)
                                            .font(.title)
                                    }
                                }
                                .frame(height: 200)
                                .onTapGesture {
                                    if let latitude = result.latitude, let longitude = result.longitude {
                                        selectedLocation = (latitude: latitude, longitude: longitude)
                                        print("Selected location set to \(latitude), \(longitude)")
                                    }
                                }


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
        .onAppear(perform: fetchInitialSearchResults)
        .navigationTitle("\(searchQuery) 검색 결과")
        .sheet(isPresented: Binding<Bool>(
            get: { selectedLocation != nil },
            set: { newValue in
                if !newValue {
                    selectedLocation = nil // 시트가 닫힐 때 selectedLocation을 nil로 설정
                }
            })
        ) {
            if let location = selectedLocation {
                FullMapView(latitude: location.latitude, longitude: location.longitude)
            }
        }

    }

    func fetchSearchResults(retryCount: Int = 3) {
        // 기존 fetchSearchResults() 함수 내용
        guard let urlString = Bundle.main.object(forInfoDictionaryKey: "API_SEARCH") as? String else {
            errorMessage = "Info.plist에서 유효하지 않은 URL"
            isLoading = false
            return
        }

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
                
                if let error = error, retryCount > 0 {
                    print("Retrying... Attempts left: \(retryCount - 1)")
                    fetchSearchResults(retryCount: retryCount - 1)
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
                            contentPreview: previewText.isEmpty ? nil : previewText,
                            latitude: response.latitude,
                            longitude: response.longitude
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
    
    func fetchInitialSearchResults() {
        fetchSearchResults()
    }



    func loadMoreResults() {
        currentPage += 1
        fetchSearchResults()
    }
}


