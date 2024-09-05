import SwiftUI

struct MenusView: View {
    @State private var menus: [Menu] = [] // 학식 메뉴 데이터를 저장하는 배열
    @State private var isLoading: Bool = true // 데이터 로딩 상태를 나타내는 변수
    @State private var errorMessage: String? = nil // 오류 메시지를 저장하는 변수
    @State private var selectedRestaurant: String = "한빛식당" // 선택된 식당
    @State private var dateRange: [Date] = [] // 월요일부터 금요일까지의 날짜 범위 저장
    @State private var selectedDate: Date = Date() // 사용자가 선택한 날짜

    let restaurants = ["한빛식당", "별빛식당", "은하수식당"] // 식당 이름 목록

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
                    VStack {
                        // 식당 선택 Picker
                        Picker("식당 선택", selection: $selectedRestaurant) {
                            ForEach(restaurants, id: \.self) { restaurant in
                                Text(restaurant).tag(restaurant)
                            }
                        }
                        .pickerStyle(SegmentedPickerStyle()) // Segmented 스타일 적용
                        .padding()

                        // 선택한 날짜 및 요일 출력
                        Text("\(formattedDate(selectedDate)) (\(formattedDayOfWeek(selectedDate)))")
                            .font(.headline)
                            .padding(.bottom, 20)

                        // 날짜 선택 TabView
                        if !dateRange.isEmpty {
                            TabView(selection: $selectedDate) {
                                ForEach(dateRange, id: \.self) { date in
                                    MenuListView(menus: menusForRestaurantAndDate(restaurant: selectedRestaurant, date: date), date: date)
                                        .tag(date) // TabView와 selectedDate를 동기화
                                }
                            }
                            .tabViewStyle(PageTabViewStyle(indexDisplayMode: .automatic)) // 페이지 스타일의 탭뷰
                        }
                    }
                }
            }
            .padding()
            .navigationTitle("학식 메뉴")
            .onAppear(perform: fetchMenus) // 뷰가 나타날 때 API 호출
        }
    }

    // 날짜와 식당에 맞는 메뉴 필터링 함수
    func menusForRestaurantAndDate(restaurant: String, date: Date) -> [Menu] {
        let dateString = formattedDate(date) // 선택한 날짜를 문자열로 변환
        return menus.filter { $0.restaurant_name == restaurant && $0.date == dateString }
    }

    // 날짜 포맷 함수 (yyyy-MM-dd 형태로 출력)
    func formattedDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: date)
    }

    // 요일을 포맷하는 함수 (월, 화 등으로 출력)
    func formattedDayOfWeek(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: "ko_KR") // 한국어로 요일 표시
        formatter.dateFormat = "EEEE" // 요일을 출력하는 포맷
        return formatter.string(from: date)
    }

    // API 호출 함수
    func fetchMenus() {
        guard let urlString = Bundle.main.object(forInfoDictionaryKey: "API_MENU") as? String,
              let url = URL(string: urlString) else {
            errorMessage = "Info.plist에서 유효하지 않은 URL"
            isLoading = false
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            DispatchQueue.main.async {
                isLoading = false

                if let error = error {
                    errorMessage = "데이터 로드 실패: \(error.localizedDescription)"
                    return
                }

                guard let data = data else {
                    errorMessage = "데이터를 받지 못했습니다"
                    return
                }

                do {
                    let decodedResponse = try JSONDecoder().decode([Menu].self, from: data)
                    self.menus = decodedResponse

                    // 받아온 메뉴 중 첫 번째 날짜를 기준으로 5일의 날짜 범위 설정
                    if let firstMenu = decodedResponse.first {
                        let startDate = stringToDate(firstMenu.date)
                        self.dateRange = generateDateRange(from: startDate, days: 5)

                        // 현재 날짜가 범위 내에 있으면 현재 날짜를 선택, 아니면 마지막 날짜 선택
                        if let validDate = validSelectedDate(from: self.dateRange) {
                            self.selectedDate = validDate
                        }
                    }

                } catch {
                    errorMessage = "데이터 파싱 실패: \(error.localizedDescription)"
                }
            }
        }.resume()
    }

    // 문자열을 Date로 변환하는 함수
    func stringToDate(_ dateString: String) -> Date {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.date(from: dateString) ?? Date() // 변환 실패 시 현재 날짜 반환
    }

    // 시작 날짜로부터 days만큼의 날짜 배열 생성 함수
    func generateDateRange(from startDate: Date, days: Int) -> [Date] {
        var dateRange: [Date] = []
        for i in 0..<days {
            if let date = Calendar.current.date(byAdding: .day, value: i, to: startDate) {
                dateRange.append(date)
            }
        }
        return dateRange
    }

    // 현재 날짜가 범위 내에 있으면 현재 날짜를 반환, 아니면 마지막 날짜 반환
    func validSelectedDate(from dateRange: [Date]) -> Date? {
        let today = Date()
        if let firstDate = dateRange.first, let lastDate = dateRange.last {
            if today >= firstDate && today <= lastDate {
                return today
            } else {
                return lastDate
            }
        }
        return nil
    }
}

// 각 날짜와 해당 식당의 메뉴 리스트를 표시하는 뷰
struct MenuListView: View {
    let menus: [Menu]
    let date: Date

    var body: some View {
        ScrollView {
            VStack(alignment: .center, spacing: 16) {
                if menus.isEmpty {
                    Text("해당 날짜에 메뉴가 없습니다.")
                        .foregroundColor(.gray)
                        .font(.body)
                } else {
                    ForEach(menus) { menu in
                        HStack {
                            VStack(alignment: .leading) {
                                Text(" \(menuTime(menu.time))")
                                    .font(.subheadline)
                                    .padding(.bottom, 2)
        
                                Text(menu.menu) // 메뉴 끝에 공백 20개 추가
                                    .font(.body)
                                    .padding(.top, 2)
                                    .multilineTextAlignment(.leading) // 텍스트 왼쪽 정렬
                            }
                            .padding()
                            .background(Color.white)
                            .cornerRadius(10)
                            .shadow(radius: 2)
                            Spacer() // 남는 공간을 채워서 가로 길이를 고정
                        }
                        .frame(minWidth: 320, maxWidth: 320, alignment: .leading)
                    }
                }
            }
            .padding()
        }
    }

    // 시간 표시를 변환하는 함수
    func menuTime(_ time: Int) -> String {
        switch time {
        case 1: return "아침"
        case 2: return "점심"
        case 3: return "저녁"
        default: return "알 수 없음"
        }
    }

    // 날짜 포맷 함수
    func formattedDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: date)
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
