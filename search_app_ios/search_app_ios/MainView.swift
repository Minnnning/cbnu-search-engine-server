import SwiftUI

struct MainView: View {
    @State private var searchQuery: String = ""
    @State private var isSearchActive: Bool = false
    @State private var searchTerms: [SearchTerm] = []

    var body: some View {
        NavigationView {
            ZStack {
                Color.appBackgroundColor
                    .ignoresSafeArea()
                
                VStack {
                    // 이미지 로고
                    Image("Image") // 로고 이미지 이름을 "Image"로 설정
                        .resizable()
                        .scaledToFit()
                        .frame(width: 230, height: 180) // 이미지 크기 조정
                        .padding(.bottom, 20) // 아래쪽 패딩 추가
                    
                    // 검색창과 버튼을 담은 HStack
                    HStack {
                        TextField("오늘의 학식?...", text: $searchQuery)
                            .padding(8)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                        
                        Button(action: {
                            if !searchQuery.isEmpty {
                                isSearchActive = true
                            }
                        }) {
                            Text("검색")
                                .font(.headline)
                                .foregroundColor(.white)
                                .padding(.horizontal)
                                .padding(.vertical, 8)
                                .background(Color.blue)
                                .cornerRadius(8)
                        }
                    }
                    .padding(.horizontal)

                    // 실시간 검색어 표시
                    VStack(alignment: .leading) {
                        Text("실시간 검색어")
                            .font(.headline)
                            .padding(.top, 20)
                        
                        ForEach(Array(searchTerms.prefix(5).enumerated()), id: \.offset) { index, term in
                            Text("\(index + 1). \(term.token) (\(term.count)회)")
                                .font(.subheadline)
                                .padding(.vertical, 2)
                        }
                    }
                    .padding(.horizontal)

                    Spacer()
                    
                    // 검색 결과 페이지로의 NavigationLink
                    NavigationLink(
                        destination: SearchResultsView(searchQuery: searchQuery), // 목적지
                        isActive: $isSearchActive,
                        label: {
                            EmptyView()
                        }
                    )
                }
                .navigationTitle("") // 타이틀을 빈 문자열로 설정하여 상단에 타이틀이 보이지 않게 설정
                .navigationBarTitleDisplayMode(.inline) // 네비게이션 바 타이틀을 인라인으로 설정
                .onAppear(perform: fetchSearchTerms) // 뷰가 나타날 때 실시간 검색어 가져오기
            }
        }
    }
    
    // API 호출 함수
    func fetchSearchTerms() {
        guard let url = URL(string: "http://127.0.0.1:8000/search-terms") else {
            print("Invalid URL")
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                print("Error fetching search terms: \(error.localizedDescription)")
                return
            }

            guard let data = data else {
                print("No data received")
                return
            }

            do {
                let decodedResponse = try JSONDecoder().decode(RealtimeSearchTermsResponse.self, from: data)
                DispatchQueue.main.async {
                    self.searchTerms = decodedResponse.realtime_search_terms
                }
            } catch {
                print("Failed to decode JSON: \(error.localizedDescription)")
            }
        }.resume()
    }
}

// API 응답 구조에 맞춘 데이터 모델
struct SearchTerm: Identifiable, Decodable {
    let id = UUID()
    let token: String
    let count: Int
}

struct RealtimeSearchTermsResponse: Decodable {
    let realtime_search_terms: [SearchTerm]
}
