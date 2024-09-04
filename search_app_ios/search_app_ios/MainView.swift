import SwiftUI

struct MainView: View {
    @State private var searchQuery: String = ""
    @State private var isSearchActive: Bool = false
    @State private var isMenuViewActive: Bool = false // '학식' 또는 '오늘의 학식'인 경우의 플래그
    @State private var searchTerms: [SearchTerm] = []

    // 타이머를 이용하여 10초마다 API를 호출하도록 설정
    private let timer = Timer.publish(every: 10, on: .main, in: .common).autoconnect()

    var body: some View {
        NavigationView {
            ZStack {
                Color.appBackgroundColor
                    .ignoresSafeArea()

                VStack {
                    // 이미지 로고
                    Image("Image")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 230, height: 180)
                        .padding(.bottom, 20)

                    // 검색창과 버튼을 담은 HStack
                    HStack {
                        TextField("오늘의 학식은?", text: $searchQuery, onEditingChanged: { isEditing in
                            if isEditing && searchQuery.isEmpty {
                                isSearchActive = false
                                isMenuViewActive = false
                            }
                        })
                        .padding(8)
                        .textFieldStyle(RoundedBorderTextFieldStyle())

                        Button(action: {
                            if searchQuery.isEmpty {
                                // 검색어가 비어 있을 경우, 플레이스홀더의 내용을 기본 검색어로 사용
                                searchQuery = "오늘의 학식"
                                isMenuViewActive = true
                            } else {
                                if searchQuery == "학식" || searchQuery == "오늘의 학식" {
                                    isMenuViewActive = true
                                } else {
                                    isSearchActive = true
                                }
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
                    VStack(alignment: .leading, spacing: 10) {
                        Text("실시간 검색어")
                            .font(.headline)
                            .padding(.top, 20)

                        ForEach(Array(searchTerms.prefix(5).enumerated()), id: \.offset) { index, term in
                            HStack {
                                Text("\(index + 1).")
                                    .font(.subheadline)
                                    .fontWeight(.bold)
                                    .foregroundColor(.gray)

                                Text(term.token)
                                    .font(.subheadline)
                                    .padding(.leading, 5)

                                Spacer()
                            }
                            .padding()
                            .background(Color.white)
                            .cornerRadius(10)
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

                    // 메뉴 페이지로의 NavigationLink
                    NavigationLink(
                        destination: MenusView(), // 목적지
                        isActive: $isMenuViewActive,
                        label: {
                            EmptyView()
                        }
                    )
                }
                .navigationTitle("") // 타이틀을 빈 문자열로 설정하여 상단에 타이틀이 보이지 않게 설정
                .navigationBarTitleDisplayMode(.inline) // 네비게이션 바 타이틀을 인라인으로 설정
                .onAppear(perform: fetchSearchTerms) // 뷰가 나타날 때 실시간 검색어 가져오기
                .onReceive(timer) { _ in
                    fetchSearchTerms() // 타이머에 따라 일정 시간마다 API 호출
                }
            }
        }
    }

    // API 호출 함수
    func fetchSearchTerms() {
        guard let url = URL(string: "http://1.248.115.71:9334/search-terms") else {
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
