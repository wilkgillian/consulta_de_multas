import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://sistemas.mt.senac.br/")
assert "Sistemas Web - Senac Mato Grosso" in driver.title
openSystem = driver.find_element(By.XPATH, "//img[@src='assets_sistemas\img\sistemas\mxm-treinamento.png']").click()
time.sleep(2)
driver.switch_to.window(driver.window_handles[1])
assert "MXM-WebManager" in driver.title
login = driver.find_element(By.ID, "txfUsuario").send_keys('WLIK.SILVA')
time.sleep(1)
driver.find_element(By.ID, "txfSenha").send_keys('Alterar@2022')
time.sleep(1)
driver.find_element(By.ID, "btnConectar").click()
time.sleep(6)

# class element_has_
# driver.find_element(By.XPATH, "//div[@class='front']")
# driver.find_element(By.XPATH, "//div[@aria-label='Fechar diálogo']").click()

time.sleep(1)

driver.find_element(By.ID, "ext-gen20").click()
time.sleep(1)
driver.find_element(By.ID, "SCB").click()
time.sleep(2)
driver.find_element(By.ID, "tgfBusca").send_keys('Acompanhamento do agendador de relatórios')
time.sleep(1)
driver.find_element(By.ID, "ext-gen907").click()
time.sleep(4)
driver.find_element(By.XPATH, "/html/body/form/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div/div/div[2]/div/table/tbody/tr[1]/td[4]/div/a").click()