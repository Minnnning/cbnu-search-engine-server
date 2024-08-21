import SwiftUI

struct MainView: View {
    @State private var searchQuery: String = ""
    @State private var isSearchActive: Bool = false

    var body: some View {
        NavigationView {
            VStack {
                TextField("Search...", text: $searchQuery)
                    .padding()
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding(.horizontal)

                Button(action: {
                    if !searchQuery.isEmpty {
                        isSearchActive = true
                    }
                }) {
                    Text("Search")
                        .font(.headline)
                        .foregroundColor(.white)
                        .padding()
                        .background(Color.blue)
                        .cornerRadius(8)
                }
                .padding(.top, 20)

                NavigationLink(
                    destination: SearchResultsView(searchQuery: searchQuery), // 목적지
                    isActive: $isSearchActive,
                    label: {
                        EmptyView()
                    }
                )
            }
            .navigationTitle("Main Page")
        }
    }
}
