import pyautogui
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import pandas as pd
from bs4 import BeautifulSoup
import re
import openpyxl

t1 = time.time()
detran = "DETRAN"
dataAtual = datetime.today()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, timeout=5000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://www16.itrack.com.br/cmatrix/controlemonitoramento")
    page.locator(
        "input[name='usuario']").fill("GEAD")
    page.locator(
        "input[name='senha']").fill("33312976")
    time.sleep(1)
    page.locator(
        "button[name='Submit']").click()
    page.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[2]/a").hover()
    page.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[2]/ul/li[2]/a").click()
    url = page.inner_html('//*[@id="box-table-b"]/tbody')
    soup = BeautifulSoup(url, 'html.parser')
    names = soup.find_all("td")
    contador = 0
    print(names)
    while contador < len(names):
        res = names[contador].text
        sec = 'SENAC'
        if res != sec and res != re.compile(r'[A-Z]'):
            print(res)
        contador +=1 
    time.sleep(10)
    browser.close()
tempoExec = time.time() - t1
print("\nTempo de execução: {} segundos".format(tempoExec))
