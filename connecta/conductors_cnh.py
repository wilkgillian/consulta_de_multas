import os
from dotenv import load_dotenv
from playwright.async_api import Page

load_dotenv()

async def conductors_cnh(page: Page, path: str):
    await page.goto(os.environ['CONNECTA'])
    await page.locator(
        "input[name='usuario']").fill(os.environ['USER_NAME'])
    await page.locator(
        "input[name='senha']").fill(os.environ['PASSWORD'])
    await page.locator(
        "button[name='Submit']").click()
    await page.locator("//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[2]/a").hover()
    await page.locator(
        "//*[@id='tabelaMenu']/tbody/tr[1]/td/ul/li[2]/ul/li[2]/a").click()
    
    ####INCOMPLETE#####
    pass