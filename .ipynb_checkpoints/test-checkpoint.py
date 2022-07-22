import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime

driver = webdriver.Chrome()
driver.get("https://sistemas.mt.senac.br/")
assert "Sistemas Web - Senac Mato Grosso" in driver.title
openSystem = driver.find_element(By.XPATH, "//img[@src='assets_sistemas\img\sistemas\sig-treinamento.png']").click()
time.sleep(2)
driver.switch_to.window(driver.window_handles[1])
assert "SENAC Portal" in driver.title
time.sleep(4)
select = Select(driver.find_element(By.TAG_NAME, "select"))
select.select_by_visible_text("DR-MT")
driver.find_element(By.XPATH, "/html/body/sig-app-root/sig-login/div[1]/div[2]/div/div[2]/sig-login-form/form/div/div[2]/button").click()
time.sleep(2)
driver.find_element(By.ID, "email").send_keys("wilk.silva@mt.senac.br")
driver.find_element(By.ID, "senha").send_keys("Alterar@2022")
time.sleep(1)
driver.find_element(By.XPATH, "/html/body/sig-app-root/sig-login/div[1]/div[2]/div/div[2]/sig-login-form/form/div/div[1]/button").click()
time.sleep(4)
driver.find_element(By.XPATH, "/html/body/sig-app-root/section/section[2]/main/sig-home/div/section[2]/div/div[1]/div/a").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='home-sig-portal-menu']/div[8]/div").click()
time.sleep(2)
driver.find_element(By.XPATH, "//*[@id='home-financeiro-menu']/div[12]/a").click()
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/sig-app-root/section/section[2]/main/sig-listar/div[2]/div/div/div/div/a[1]/div/div/div/div[2]").click()
situacao = Select(driver.find_element(By.XPATH, "/html/body/sig-app-root/section/section[2]/main/sig-receita-a-receber/div/div/div[2]/div/form/div[1]/div[1]/sig-input/div/select"))
situacao.select_by_visible_text("Vencida")
unidade = driver.find_element(By.XPATH, "/html/body/sig-app-root/section/section[2]/main/sig-receita-a-receber/div/div/div[2]/div/form/div[1]/div[2]/div/sig-typeahead/div/div[1]/div[1]/input").click()
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/sig-app-root/section/section[2]/main/sig-receita-a-receber/div/div/div[2]/div/form/div[1]/div[2]/div/sig-typeahead/div/div[3]/ul/li[1]").click()
filtro = Select(driver.find_element(By.XPATH, "/html/body/sig-app-root/section/section[2]/main/sig-receita-a-receber/div/div/div[2]/div/form/div[2]/div[1]/sig-input/div/select"))
filtro.select_by_visible_text("Posição e Período")
comBase = Select(driver.find_element(By.XPATH, "/html/body/sig-app-root/section/section[2]/main/sig-receita-a-receber/div/div/div[2]/div/form/div[2]/div[2]/sig-input/div/select"))
comBase.select_by_visible_text("Pagamento")
dataAtual = datetime.today()
formatData = dataAtual.strftime("%d/%m/%Y")
posicao = driver.find_element(By.ID, "calendar").send_keys(str(formatData))
comRelacao = Select(driver.find_element(By.XPATH, "/html/body/sig-app-root/section/section[2]/main/sig-receita-a-receber/div/div/div[2]/div/form/div[3]/div[1]/sig-input/div/select"))
comRelacao.select_by_visible_text("Data de Vencimento")
formatInitialDate = dataAtual.strftime("01/%m/%Y")
vencimentoInicial = driver.find_element(By.ID, "dataInicio").click()
pyautogui.write(str(formatInitialDate))
time.sleep(1)
vencimentoFinal =  driver.find_element(By.ID, "dataFinal").click()
pyautogui.write(str(formatData))
time.sleep(1)
tipoDeArquivo = Select(driver.find_element(By.XPATH, "/html/body/sig-app-root/section/section[2]/main/sig-receita-a-receber/div/div/div[2]/div/form/div[3]/div[4]/sig-formato-de-impressao/div/sig-input/div/select"))
tipoDeArquivo.select_by_visible_text("PDF")
jurosCurrent = driver.find_element(By.XPATH, "/html/body/sig-app-root/section/section[2]/main/sig-receita-a-receber/div/div/div[2]/div/form/div[4]/div[1]/label").click()
generate = driver.find_element(By.XPATH, "/html/body/sig-app-root/section/section[2]/main/sig-receita-a-receber/div/div/div[2]/div/form/div[4]/div[2]/div/button[2]").click()
time.sleep(1)
driver.find_element(By.XPATH, "/html/body/div/div/div[3]/button[1]").click()

##computador##

time.sleep(60)

pyautogui.press('win')
pyautogui.write('meu computador')
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)
pyautogui.write('downloads')
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)
pyautogui.write('ReceitaAReceber')
time.sleep(1)

sys.exit()
exit()