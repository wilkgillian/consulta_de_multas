import re
from bs4 import BeautifulSoup


def extractor_licenciamento(url):
    soupLicenciamento = BeautifulSoup(
        url, 'html.parser')
    licenciamentoArray = soupLicenciamento.find_all(
        'td', attrs={'width': False, 'colspan': False})
    liceContador = 0
    while liceContador < len(licenciamentoArray):
        res = licenciamentoArray[liceContador].text
        if re.search("Licenciamento", res):
            licenciamentoRes = res
            vencimentoLicenciamento = licenciamentoArray[liceContador+1].text

        liceContador += 1
    # não finalizado necessita de um débito para teste
    return {"licenciamento": licenciamentoRes, "vencimento_licenciamento": vencimentoLicenciamento}


def extractor_infracoes_em_autuacao(url):
    soup = BeautifulSoup(url, 'html.parser')
    debitos = soup.find_all(
        'td', attrs={'class': False, 'width': False, 'colspan': False})
    i = 0
    while i < len(debitos):
        local = debitos[0].text
        data = debitos[1].text
        i += 1
    return {"local": local, "data": data}


def extractor_penalidades(url):
    soup = BeautifulSoup(url, 'html.parser')
    debitos = soup.find_all(
        'td', attrs={'class': False, 'width': False, 'colspan': False})
    i = 0
    while i < len(debitos):
        local = debitos[0].text
        data = debitos[1].text
        i += 1
    return {"local": local, "data": data}
