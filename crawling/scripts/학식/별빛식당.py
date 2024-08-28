# cafeteria_byulbit.py

from menu_scraper import CafeteriaScraper

# Instantiate the scraper for 별빛식당
cafeteria_byulbit = CafeteriaScraper(
    url="https://www.cbnucoop.com/service/restaurant/",
    tab=2,
    cafeteria_id=2,
    cafeteria_name="별빛식당"
)

# Run the scraper and print results
menus = cafeteria_byulbit.run()
print(f"Results for {cafeteria_byulbit.cafeteria_name}:")
for menu in menus:
    print(menu)
print()
