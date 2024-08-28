# cafeteria_eunhasu.py

from menu_scraper import CafeteriaScraper

# Instantiate the scraper for 은하수식당
cafeteria_eunhasu = CafeteriaScraper(
    url="https://www.cbnucoop.com/service/restaurant/",
    tab=3,
    cafeteria_id=3,
    cafeteria_name="은하수식당"
)

# Run the scraper and print results
menus = cafeteria_eunhasu.run()
print(f"Results for {cafeteria_eunhasu.cafeteria_name}:")
for menu in menus:
    print(menu)
print()
