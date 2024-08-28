import SwiftUI

struct ContentView: View {
    var body: some View {
        MainView()
            .background(Color.appBackgroundColor) // 배경색
    }
}

extension Color {
    static let appBackgroundColor = Color(red: 248/255, green: 253/255, blue: 254/255)
}
