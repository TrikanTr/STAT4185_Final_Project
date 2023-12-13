import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import sqlite3


def highlight(element, color, border):
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
    original_style = element.get_attribute('style')
    apply_style("border: {0}px solid {1};".format(border, color))
    time.sleep(0.1)
    apply_style(original_style)


conn = sqlite3.connect("pokemon.db")

cur = conn.cursor()

cur.execute("""CREATE TABLE poke_info (
        name TEXT,
        usage TEXT,
        type1 TEXT,
        type2 TEXT,
        BST integer,
        HP integer,
        ATK integer,
        DEF integer,
        SPA integer,
        SPD integer,
        SPE integer,
        item TEXT
    )""")

PATH = '/Users/prathiamo/Coding_classes/STAT_4185/git_github/STAT4185_Final_Project/chromedriver-mac-x64/chromedriver'
services = Service(PATH)
driver = webdriver.Chrome(service=services)
driver.get('https://pokestats.pucko.info/pokeStats/?format=gen9ou&time=month')
time.sleep(2)



def get_all_info(selector, poke_list):
    temp_lst = []
    row = driver.find_element(By.CSS_SELECTOR, selector)
    highlight(row, "red", 5)
    poke_link = row.find_element(By.CSS_SELECTOR, "a")

    poke_link.click()
    
    poke_name = driver.find_element(By.CSS_SELECTOR, ".box div:nth-child(1) h3:nth-child(1)")
    highlight(poke_name, "red", 5)
    if poke_name.text == "Walking_Wake":
        driver.back()
        return
    temp_lst.append(poke_name.text)
    
    
    usage = driver.find_element(By.CSS_SELECTOR, "#main_image~ h3")
    highlight(usage, "red", 5)
    temp_lst.append(usage.text)
    
    type_list = ["Normal", "Water", "Fire", "Grass", "Electric", "Fighting", "Flying", "Bug", "Rock", "Ground", "Poison", "Psychic", "Dark", "Ghost", "Ice", "Dragon", "Steel", "Fairy"]
    
    type1_raw = driver.find_element(By.CSS_SELECTOR, "h3+ p:nth-child(2)")
    highlight(type1_raw, "red", 5)
    temp_lst.append(type1_raw.text)


    try:
        type2_raw = driver.find_element(By.CSS_SELECTOR, ".box div div div div:nth-child(2) p~ p+ p")
    
    except:
        temp_lst.append("None")

    else:
        highlight(type2_raw, "red", 5)
        if type2_raw.text in type_list: 
            temp_lst.append(type2_raw.text)
        else:
            temp_lst.append("None")

    stats = driver.find_elements(By.CSS_SELECTOR, "div:nth-child(4) p")
    for stat in stats:
        highlight(stat, "red", 5)
        temp_lst.append(stat.text)

    top_item = driver.find_element(By.CSS_SELECTOR, ".table-data+ .table-data tr:nth-child(1) td:nth-child(2)")
    highlight(top_item, "red", 5)
    temp_lst.append(top_item.text)
    
    poke_list.append(tuple(temp_lst))
    driver.back()
    return



action = ActionChains(driver)

poke_list = []

for i in range(1, 200):
    if i == 20 or i==25 or i==147 or i==192:
        continue
    selector = "tr:nth-child(" + str(i) + ") td , tr:nth-child(" + str(i) + ") td+ td .button"
    get_all_info(selector, poke_list)
    target = driver.find_element(By.CSS_SELECTOR,"td")
    time.sleep(2)

cur.executemany("INSERT INTO poke_info VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", poke_list,)
conn.commit()
conn.close()
time.sleep(2)

driver.close()