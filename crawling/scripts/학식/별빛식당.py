from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import datetime

# Initialize WebDriver (Make sure to download the appropriate WebDriver for your browser)
driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.

# Navigate to the URL
url = "https://www.cbnucoop.com/service/restaurant/"
driver.get(url)

# Wait for the menu table to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#menu-table")))

# Click on the desired tab
tabs = driver.find_elements(By.CSS_SELECTOR, "#restaurant-menu > div.navbar.navbar-bg.mb-3.nav.nav-pills > nav > a")
tabs[2 - 1].click()  # tab index is 2 in the original script, but Python uses 0-based indexing

# Wait for the content to load after clicking the tab
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".active table > tbody > tr")))

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Locate the week menus and weekday titles
week_menus = soup.select(".active table > tbody > tr")
week_titles = soup.select(".weekday-title")

result = []

time = 1

for week_menu_index, week_menu in enumerate(week_menus):
    if '아점' in week_menu.text or '아침' in week_menu.text:
        time = 1
    elif '점심' in week_menu.text or '중식' in week_menu.text:
        time = 2
    elif '저녁' in week_menu.text or '석식' in week_menu.text:
        time = 3

    if week_menu_index % 2 == 1:
        days = week_menu.find_all("td")

        for index, day in enumerate(days):
            try:
                if day.find(class_="card-header"):
                    MMDD = week_titles[index].text.replace(
                        "(월요일)", "").replace("(화요일)", "").replace("(수요일)", "").replace("(목요일)", "").replace("(금요일)", "")
                    main_menu = day.find(class_="card-header").text
                    sub_menus = " ".join([m.text for m in day.select(".card-body .side")])
                    menu = f"{main_menu} {sub_menus}".replace("\n", "").strip()

                    if menu != "" and menu != ".":
                        result.append({
                            'id': None,  # `id` was not clearly defined in the original script
                            'cafeteriaId': 5,
                            'cafeteria_name': "별빛식당",
                            'menu': menu,
                            'time': time,
                            'date': f"{datetime.datetime.now().year}.{MMDD.strip()}"
                        })
            except Exception as e:
                print(e, day)

# Output the results
for item in result:
    print(item)

# Close the WebDriver
driver.quit()
