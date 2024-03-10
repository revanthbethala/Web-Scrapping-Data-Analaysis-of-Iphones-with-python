from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Chrome()

color,title,price,rating,offer=[],[],[],[],[]

for page in range(1,22):
    url=f"https://www.flipkart.com/search?q=apple+phones&page={page}"
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div._4rR01T")))

    titles=driver.find_elements(By.CSS_SELECTOR, "div._4rR01T")
    prices=driver.find_elements(By.CSS_SELECTOR, "div._30jeq3._1_WHN1")
    ratings=driver.find_elements(By.CSS_SELECTOR, "div._3LWZlK")
    offers=driver.find_elements(By.CSS_SELECTOR, "div._3Ay6Sb")

    for i in range(len(titles)):
        title_text = titles[i].text
        start = title_text.find("(")+1
        end = title_text.find(",")
        colors = title_text[start:end]
        color.append(colors)
        title.append(title_text[:title_text.index("(")].strip() if i < len(titles) else 'N/A')
        price.append(prices[i].text[1:].replace(",","").strip() if i < len(prices) else 'N/A')
        rating.append(ratings[i].text.strip() if i < len(ratings) else 'N/A')
        if i < len(offers):
            offer_text = offers[i].text
            offer.append(offer_text[:offer_text.find("%")].strip() if offers[i].text != "" else '0')
        else:
            offer.append("0")


price = [int(p) for p in price]
offer = [float(o) for o in offer]
rating = [float(r) for r in rating]
driver.close()

df=pd.DataFrame({
    'Title':title,
    "Color":color,
    'Price':price,
    'Rating':rating,
    'Offer':offer
})

df.to_csv('iphones.csv',index=False)