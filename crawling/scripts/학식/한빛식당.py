# cafeteria_hanbit.py

from menu_scraper import CafeteriaScraper

# Instantiate the scraper for 한빛식당
cafeteria_hanbit = CafeteriaScraper(
    url="https://www.cbnucoop.com/service/restaurant/",
    tab=1,
    cafeteria_id=1,
    cafeteria_name="한빛식당"
)

# Run the scraper and print results
menus = cafeteria_hanbit.run()
print(f"Results for {cafeteria_hanbit.cafeteria_name}:")
for menu in menus:
    print(menu)
print()
