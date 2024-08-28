import SwiftUI

struct MainView: View {
    @State private var searchQuery: String = ""
    @State private var isSearchActive: Bool = false

    var body: some View {
        NavigationView {
            ZStack{
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
                        TextField("Search...", text: $searchQuery)
                            .padding(8)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                        
                        Button(action: {
                            if !searchQuery.isEmpty {
                                isSearchActive = true
                            }
                        }) {
                            Text("Search")
                                .font(.headline)
                                .foregroundColor(.white)
                                .padding(.horizontal)
                                .padding(.vertical, 8)
                                .background(Color.blue)
                                .cornerRadius(8)
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
            }
        }
    }
}
