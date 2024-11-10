//FullMapView
import SwiftUI
import MapKit

struct FullMapView: View {
    var latitude: Double
    var longitude: Double
    
    @Environment(\.dismiss) var dismiss

    var body: some View {
        NavigationView {
            Map(coordinateRegion: .constant(MKCoordinateRegion(
                center: CLLocationCoordinate2D(latitude: latitude, longitude: longitude),
                span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
            )), annotationItems: [MapPin(coordinate: CLLocationCoordinate2D(latitude: latitude, longitude: longitude))]) { location in
                MapAnnotation(coordinate: location.coordinate) {
                    Image(systemName: "mappin")
                        .foregroundColor(.red)
                        .font(.title)
                }
            }
            .edgesIgnoringSafeArea(.bottom)
            .navigationTitle("지도 보기")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("닫기") {
                        dismiss()
                    }
                }
            }
        }
    }
}
