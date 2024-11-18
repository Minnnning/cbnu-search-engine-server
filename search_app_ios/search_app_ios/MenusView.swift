import SwiftUI

struct MenusView: View {
    @State private var menus: [Menu] = []
    @State private var isLoading: Bool = true
    @State private var errorMessage: String? = nil
    @State private var selectedRestaurant: String = "한빛식당"
    @State private var dateRange: [Date] = []
    @State private var selectedDate: Date = Date()

    let restaurants = ["한빛식당", "별빛식당", "은하수식당"]

    var body: some View {
        ZStack {
            Color.appBackgroundColor.ignoresSafeArea()
            VStack {
                if isLoading {
                    ProgressView("Loading...")
                } else if let errorMessage {
                    Text("Error: \(errorMessage)").foregroundColor(.red)
                } else {
                    menuContent
                }
            }
            .padding()
            .navigationTitle("학식 메뉴")
            .onAppear(perform: fetchMenus)
        }
    }

    private var menuContent: some View {
        VStack {
            Picker("식당 선택", selection: $selectedRestaurant) {
                ForEach(restaurants, id: \.self) { Text($0).tag($0) }
            }
            .pickerStyle(SegmentedPickerStyle())
            .padding()

            Text("\(formattedDate(selectedDate)) (\(formattedDayOfWeek(selectedDate)))")
                .font(.headline)
                .padding(.bottom, 20)

            if !dateRange.isEmpty {
                TabView(selection: $selectedDate) {
                    ForEach(dateRange, id: \.self) { date in
                        MenuListView(
                            menus: menusForRestaurantAndDate(restaurant: selectedRestaurant, date: date),
                            date: date
                        )
                        .tag(date)
                    }
                }
                .tabViewStyle(PageTabViewStyle(indexDisplayMode: .automatic))
            }

            Spacer()
            Text("<<      좌우로 넘기세요      >>")
                .font(.footnote)
                .foregroundColor(.gray)
                .padding(.bottom, 20)
        }
    }

    func menusForRestaurantAndDate(restaurant: String, date: Date) -> [Menu] {
        let dateString = formattedDate(date)
        return menus.filter { $0.restaurant_name == restaurant && $0.date == dateString }
    }

    func formattedDate(_ date: Date) -> String {
        DateFormatter.shared.string(from: date, format: "yyyy-MM-dd")
    }

    func formattedDayOfWeek(_ date: Date) -> String {
        DateFormatter.shared.string(from: date, format: "EEEE", locale: Locale(identifier: "ko_KR"))
    }

    func fetchMenus() {
        guard let urlString = Bundle.main.object(forInfoDictionaryKey: "API_MENU") as? String,
              let url = URL(string: urlString) else {
            updateErrorMessage("Info.plist에서 유효하지 않은 URL")
            return
        }

        URLSession.shared.dataTask(with: url) { data, _, error in
            DispatchQueue.main.async {
                isLoading = false
                if let error {
                    updateErrorMessage("데이터 로드 실패: \(error.localizedDescription)")
                } else if let data, let decodedMenus = try? JSONDecoder().decode([Menu].self, from: data) {
                    processFetchedMenus(decodedMenus)
                } else {
                    updateErrorMessage("데이터를 받지 못했습니다")
                }
            }
        }.resume()
    }

    func processFetchedMenus(_ fetchedMenus: [Menu]) {
        menus = fetchedMenus
        if let firstDate = fetchedMenus.first.flatMap({ stringToDate($0.date) }) {
            dateRange = generateDateRange(from: firstDate, days: 5)
            
            // 현재 날짜가 범위 내에 있으면 선택, 아니면 첫 번째 날짜를 선택
            selectedDate = validSelectedDate(from: dateRange) ?? dateRange.first ?? Date()
        }
    }

    func updateErrorMessage(_ message: String) {
        errorMessage = message
        isLoading = false
    }

    func stringToDate(_ dateString: String) -> Date {
        DateFormatter.shared.date(from: dateString, format: "yyyy-MM-dd") ?? Date()
    }

    func generateDateRange(from startDate: Date, days: Int) -> [Date] {
        (0..<days).compactMap { Calendar.current.date(byAdding: .day, value: $0, to: startDate) }
    }

    func validSelectedDate(from dateRange: [Date]) -> Date? {
        let today = Calendar.current.startOfDay(for: Date())
        return dateRange.first { Calendar.current.isDate($0, inSameDayAs: today) }
    }
}

struct MenuListView: View {
    let menus: [Menu]
    let date: Date

    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                if menus.isEmpty {
                    Text("해당 날짜에 메뉴가 없습니다.")
                        .foregroundColor(.gray)
                        .font(.body)
                } else {
                    ForEach(menus) { menu in
                        MenuItemView(menu: menu)
                    }
                }
            }
            .padding()
        }
    }
}

struct MenuItemView: View {
    let menu: Menu

    var body: some View {
        VStack(alignment: .leading) {
            Text(menuTime(menu.time))
                .font(.headline)
                .padding(.bottom, 2)
                .frame(maxWidth: .infinity, alignment: .leading)

            Text(menu.menu)
                .font(.body)
                .padding(.top, 2)
        }
        .padding()
        .background(Color.white)
        .cornerRadius(10)
        .shadow(radius: 2)
    }

    func menuTime(_ time: Int) -> String {
        ["알 수 없음", "아침", "점심", "저녁"][min(max(time, 0), 3)]
    }
}

struct Menu: Identifiable, Decodable {
    let id: Int
    let restaurantId: Int
    let restaurant_name: String
    let menu: String
    let time: Int
    let date: String
}

extension DateFormatter {
    static let shared = DateFormatter()

    func string(from date: Date, format: String, locale: Locale = .current) -> String {
        self.dateFormat = format
        self.locale = locale
        return self.string(from: date)
    }

    func date(from string: String, format: String) -> Date? {
        self.dateFormat = format
        return self.date(from: string)
    }
}

#Preview {
    MenusView()
}
