import SwiftUI

struct MainView: View {
    @State private var searchQuery: String = ""
    @State private var isSearchActive: Bool = false
    @State private var isMenuViewActive: Bool = false // '학식' 또는 '오늘의 학식'인 경우의 플래그
    @State private var searchTerms: [SearchTerm] = []
    @State private var isLoading: Bool = true // 데이터 로딩 상태를 나타내는 변수
    @State private var errorMessage: String? = nil // 오류 메시지를 저장하는 변수

    // 타이머를 이용하여 20초마다 API를 호출하도록 설정
    private let timer = Timer.publish(every: 100, on: .main, in: .common).autoconnect()

    var body: some View {

        GeometryReader { geometry in
            NavigationStack {
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
                                performSearch()
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
                                    
                                    // 검색어 클릭 이벤트 처리 (검은색 텍스트)
                                    Text(term.token)
                                        .font(.subheadline)
                                        .foregroundColor(.black) // 검은색 텍스트로 설정
                                        .padding(.leading, 5)
                                        .onTapGesture {
                                            searchQuery = term.token
                                            performSearch()
                                        }
                                    
                                    Spacer()
                                }
                                .padding()
                                .background(Color.white)
                                .cornerRadius(10)
                                .shadow(radius: 2)
                            }
                        }
                        .padding(.horizontal)
                        
                        Spacer()
                    }
                    .frame(maxWidth: min(geometry.size.width, 500))
                    .onAppear(perform: fetchSearchTerms) // 뷰가 나타날 때 실시간 검색어 가져오기
                    .onReceive(timer) { _ in
                        fetchSearchTerms() // 타이머에 따라 일정 시간마다 API 호출
                    }
                    .navigationDestination(isPresented: $isSearchActive) {
                        SearchResultsView(searchQuery: searchQuery)
                    }
                    .navigationDestination(isPresented: $isMenuViewActive) {
                        MenusView()
                    }
                }
            }
                .frame(width: geometry.size.width, height: geometry.size.height)
        }
    }

    // 검색을 수행하는 함수
    func performSearch() {
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
    }

    // API 호출 함수
    func fetchSearchTerms() {
        // 'Info.plist'에서 URL 가져오기
        guard let urlString = Bundle.main.object(forInfoDictionaryKey: "API_SEARCH_TERM") as? String,
              let url = URL(string: urlString) else {
            errorMessage = "Info.plist에서 유효하지 않은 URL"
            isLoading = false
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
            // 서버로부터 받은 실제 데이터를 출력하여 확인
                //print("Received data: \(String(data: data, encoding: .utf8) ?? "No readable data")")

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

#Preview {
    MainView()
}
