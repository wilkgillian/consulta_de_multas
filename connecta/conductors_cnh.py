import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import Page

from connecta.extractors_connecta import extractor_condutores


load_dotenv()


async def conductors_cnh(page: Page, path):
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
    try:
        page.set_default_timeout(2000)
        url = await page.inner_html(
            '//*[@id="box-table-b"]/tbody/tr[16]/th/form')
        soup = BeautifulSoup(url, 'html.parser')
        next_page = soup.find('a').get('href')

        while next_page is not None:
            try:
                # url_to_extract = await page.inner_html('//*[@id="box-table-b"]/tbody')
                await extractor_condutores(page=page, path=path)
                await page.locator(
                    "//*[@id='box-table-b']/tbody/tr[16]/th/form/a", has_text="Próxima").click()
            except:
                next_page = None
    except:
        print("Single page")

    await page.close()
    pass
