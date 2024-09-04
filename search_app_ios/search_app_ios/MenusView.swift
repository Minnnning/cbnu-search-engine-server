import SwiftUI

struct MenusView: View {
    @State private var menus: [Menu] = [] // 학식 메뉴 데이터를 저장하는 배열
    @State private var isLoading: Bool = true // 데이터 로딩 상태를 나타내는 변수
    @State private var errorMessage: String? = nil // 오류 메시지를 저장하는 변수
    
    var body: some View {
        ZStack {
            Color.appBackgroundColor
                .ignoresSafeArea()

            VStack {
                if isLoading {
                    ProgressView("Loading...")
                } else if let errorMessage = errorMessage {
                    Text("Error: \(errorMessage)").foregroundColor(.red)
                } else {
                    List(menus) { menu in
                        VStack(alignment: .leading) {
                            Text(menu.restaurant_name)
                                .font(.headline)
                                .padding(.bottom, 2)
                            
                            Text("날짜: \(menu.date)")
                                .font(.subheadline)
                                .foregroundColor(.gray)
                            
                            Text(menu.menu)
                                .font(.body)
                                .padding(.top, 2)
                        }
                        .padding()
                        .background(Color.white)
                        .cornerRadius(10)
                        .shadow(radius: 2)
                    }
                }
            }
            .padding()
            .navigationTitle("학식 메뉴")
            .onAppear(perform: fetchMenus) // 뷰가 나타날 때 API 호출
        }
    }
    
    // API 호출 함수
    func fetchMenus() {
        guard let url = URL(string: "http://1.248.115.71:9334/menus") else {
            errorMessage = "Invalid URL"
            isLoading = false
            return
        }

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
                    let decodedResponse = try JSONDecoder().decode([Menu].self, from: data)
                    self.menus = decodedResponse
                } catch {
                    errorMessage = "Failed to parse data: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
}

// API 응답 구조에 맞춘 데이터 모델
struct Menu: Identifiable, Decodable {
    let id: Int
    let restaurantId: Int
    let restaurant_name: String
    let menu: String
    let time: Int
    let date: String
}

#Preview {
    MenusView()
}
