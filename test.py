import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
import pandas as pd


dataAtual = datetime.today()
formatData = dataAtual.strftime("%d/%m/%Y").replace("/", "-")
planilha = pd.read_excel("C:/Users/wilkw/Downloads/Controle - Frota.xlsx", "Vencimento Documentação", usecols=[8, 9])
planilha.to_excel("C:/Users/wilkw/Downloads/Consulta dia "+formatData+".xlsx")
planilha_formatada = pd.read_excel("C:/Users/wilkw/Downloads/Consulta dia "+formatData+".xlsx")
for index,row in planilha_formatada.iterrows():
    driver = webdriver.Chrome()
    driver.get("https://www.detran.mt.gov.br/")
    time.sleep(2)
    assert "Início - DETRAN" in driver.title
    openSystem = driver.find_element(By.XPATH, "//*[@id='myPopup']/span").click()
    time.sleep(2)
    print("index: "+str(index)+" e a placa é "+row["PLACA"])
    placa = row["PLACA"]
    renavan = row["RENAVAN"]
    driver.find_element(By.ID, "input_placa").send_keys(placa)
    driver.find_element(By.ID, "input_renavam").send_keys(int(renavan))
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[@id='formVeiculo']/div[4]/input[2]").click()
    driver.switch_to.window(driver.window_handles[1])
    # assert "DetranNet - Extrato do Veículo de PLACA "+placa+"" in driver.title
    select = Select(driver.find_element(By.ID, "cmbTipoDebito"))
    select.select_by_visible_text("Multas").click()
# # time.sleep(1)
# driver.switch_to.window(driver.window_handles[1])
# print("Linha "+str(index)+" Coluna "+str(row)+" \n")
    driver.quit
# planilha.to_excel("C:/Users/wilk.silva/Downloads/Consulta dia "+formatData+".xlsx")