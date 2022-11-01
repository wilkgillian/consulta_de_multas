from bs4 import BeautifulSoup

def extractor_licenciamento():
    licenciamento = 1
    vencimento = 2
    return licenciamento, vencimento   

 
def extractor_infracoes_em_autuacao(url):
    soup = BeautifulSoup(url, 'html.parser')
    debitos = soup.find_all(
        'td', attrs={'class': False, 'width': False, 'colspan': False})
    i=0
    while i < len(debitos):
        local = debitos[0].text
        data = debitos[1].text
        i+=1
    return {"local": local, "data": data}
# , data
def extractor_penalidades():
    pass