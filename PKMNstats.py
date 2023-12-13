import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import sqlite3
import pandas as pd

con = sqlite3.connect("pokemon.db")
df = pd.read_sql_query("SELECT * from poke_info", con)

print(df)

con.close()