# %% 
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

qntd_noticias = 50
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,en-US;q=0.7,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    # 'Cookie': 'cookie-banner-consent-accepted=false; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIEYOBWAJh44A2QQAYRADgAsggMyjJAdhABfIA; _pcid=%7B%22browserId%22%3A%22meafp4orhseb2viq%22%7D; xbc=%7Bkpex%7DL1JHFU6Xo4Mf-C8rYQ0XsW7uxbHEJIFRdmq6z6kwVV5nA4Cxu_5BYPlgaj6lrpv_wJiM8o6LzB7Xjlgiqdh-Dz7C0F8TiZ7i1QizdOl5GGwF9vdQHFPzLHwV6cw0SnmUewBZ840yNKc-z1AEedzEDm-gZc1vM82KCWeim2wVcN2-hJklVgOACAFGCFF-5h_yrJWw4PaSfAI7-H1FeET8dj84vVlS8D5MbPOzgSXLNlUmTEprjZ8Tom0pBtWgjxUdKDTy5pNbRwBSyhmk0U-6jeIpQ0UUfWswXGq08eZ_iKT6p_7uhWOVLShF5Zsyt1BceCRl7Mn_EDnBScJlmF8WYw; _pcus=eyJ1c2VyU2VnbWVudHMiOnsiQ09NUE9TRVIxWCI6eyJzZWdtZW50cyI6WyJMVHM6ODNmZDM5NjNlMzg3M2NkYjZiMDg3MjBkNWNkZGYwODk5OTgxZGUxMDpub19zY29yZSJdfX19; _pc_randomCookieForPiano=cookieB; __pat=-10800000; __tbc=%7Bkpex%7DUdmkXHS-TIPju1QycNOmMJTI8CyOPaPeZR8ZGRb88NnOfe97V6sqLXT1dCNQV9W9; glb_uid="S_gxUipRQs3jMNxXQp8kWFvfT1weWtv3McUpaPxMXIM="; _ga=1.1; glbExpIdToken=',
    'Priority': 'u=0, i',
}

sitemap_g1 = "https://g1.globo.com/rss/g1/educacao/"
sitemap_uol = "https://noticias.uol.com.br/sitemap/v2/today.xml"
sitemap_r7 = "https://www.r7.com/arc/outboundfeeds/sitemap/latest/"

def get_sitemap(url):
    response_sitemap = requests.get(url, headers=headers)
    if response_sitemap.status_code !=200:
        print("Sitemap não carregado", url)
        return None
    else:
        soup = BeautifulSoup(response_sitemap.text, features="xml")
        return  soup

def get_dados_g1(all_itens_g1):

    links_g1 = []
    title_g1 = []
    subtitle_g1 = []
    date_iso_g1 =[]

    for item in all_itens_g1 [:qntd_noticias]:

        link_tag = item.find('link')
        if link_tag:
            links_g1.append(link_tag.text)
        else:
            links_g1.append(None)

        title_tag = item.find('title')
        if title_tag:
            title_g1.append(title_tag.text)
        else:
            title_g1.append(None)

        subtitle_tag = item.find('atom:subtitle')
        if subtitle_tag:
            subtitle_g1.append(subtitle_tag.text)
        else:
            subtitle_g1.append(title_tag.text)

        data_tag = item.find('pubDate')
        if data_tag:
            data_tag = data_tag.text
            dt = datetime.strptime(data_tag,"%a, %d %b %Y %H:%M:%S %z")
            data_tag = dt.isoformat()
            date_iso_g1.append(data_tag)
        else:
            date_iso_g1.append(None)

    dados_g1={
    "Veiculo":["G1"] * len(links_g1),
    "Link da matéria" : links_g1,
    "Título da Matéria" : title_g1,
    "Subtítulo" : subtitle_g1,
    "Data(ISO)" : date_iso_g1,
    }

    return dados_g1    

def get_itens_uol_r7(soup):
    all_itens = soup.find_all('url')
    return all_itens

def get_links_uol_r7(all_itens):
    links_uol_r7 = []
    for item in all_itens[:qntd_noticias]:
        link_tag = item.find('loc')
        if link_tag:
            links_uol_r7.append(link_tag.text)
        else:
            links_uol_r7.append(None)
    return links_uol_r7

def get_dados_uol(links_uol_r7):
    title_uol = []
    subtitle_uol = []
    date_iso_uol =[]

    for link in links_uol_r7[:qntd_noticias]:
        resp_inside_uol = requests.get(link, headers=headers)  
        soup = BeautifulSoup(resp_inside_uol.content, "html.parser")
        
        if "newsletters" in link:
                title_tag = soup.find("td", class_ ="title")
                if title_tag:
                    title_uol.append(title_tag.text.strip())
                else:
                    title_tag = soup.find("h1", class_ ="headline")
                    if title_tag:
                        title_uol.append(title_tag.text.strip())
                    else:
                        title_uol.append(None)

                subtitle_tag = soup.find("td", class_="manchete-texto")
                if subtitle_tag:
                    subtitle_tag = subtitle_tag.find_all("p")[0]
                    subtitle_uol.append(subtitle_tag.text.strip())
                else:
                    subtitle_uol.append(None)

                date_tag = soup.find("time", class_="date") 
                if date_tag and date_tag.has_attr("datetime"):
                    date_iso_uol.append(date_tag["datetime"])
                else:
                    date_iso_uol.append(None)

        else:
                title_tag = soup.find("h1")
                if title_tag:
                    title_uol.append(title_tag.text.strip())
                else:
                    title_uol.append(None)

                subtitle_tag = soup.find("meta", property="og:description")
                if subtitle_tag:
                    subtitle_uol.append(subtitle_tag["content"].strip())
                else:
                    subtitle_uol.append(None)

                date_tag = soup.find("time", class_="date") 
                if date_tag and date_tag.has_attr("datetime"):
                    date_iso_uol.append(date_tag["datetime"])
                else:
                    date_iso_uol.append(None)

    dados_uol={
        "Veiculo" : ["Uol"] * len(links_uol_r7 ),
        "Link da matéria" : links_uol_r7,
        "Título da Matéria" : title_uol,
        "Subtítulo" : subtitle_uol,
        "Data(ISO)" : date_iso_uol,
        }
    return dados_uol

def get_dados_r7(links_r7):
    title_r7 = []
    subtitle_r7 = []
    date_iso_r7 =[]

    for link in links_r7[:qntd_noticias]:
        resp_inside_r7 = requests.get(link, headers=headers) 
        soup = BeautifulSoup(resp_inside_r7.content, "html.parser")

        title_tag = soup.find("h1")
        if title_tag:
            title_r7.append(title_tag.text.strip())
        else:
            title_r7.append(None)


        subtitle_tag = soup.find("h2")
        if subtitle_tag:
            subtitle_r7.append(subtitle_tag.text.strip())
        else:
            subtitle_r7.append(None)


        date_tag = soup.find("time") 
        if date_tag and date_tag.has_attr("datetime"):
            date_iso_r7.append(date_tag["datetime"])
        else:
            date_iso_r7.append(None)

    data_r7={
        "Veiculo" : ["R7"] * len(links_r7),
        "Link da matéria" : links_r7,
        "Título da Matéria" : title_r7,
        "Subtítulo" : subtitle_r7,
        "Data(ISO)" : date_iso_r7,
        }
    return data_r7

def export_csv(d_g1,d_uol,d_r7):
    df_geral = pd.concat([
        pd.DataFrame(d_g1),
        pd.DataFrame(d_uol),
        pd.DataFrame(d_r7)
    ], ignore_index=True)

    return df_geral.to_csv("result.csv", index=False, sep=";")

start_time = datetime.now()

#g1
soup_g1 = get_sitemap(sitemap_g1)
all_itens_g1 = soup_g1.find_all('item')
dados_g1 = get_dados_g1(all_itens_g1)

# uol
soup_uol = get_sitemap(sitemap_uol)
all_itens_uol = get_itens_uol_r7(soup_uol)
links_uol = get_links_uol_r7(all_itens_uol)
dados_uol = get_dados_uol(links_uol)

# R7
soup_r7 = get_sitemap(sitemap_r7)
all_items_r7 = get_itens_uol_r7(soup_r7)
links_r7 = get_links_uol_r7(all_items_r7)
dados_r7 = get_dados_r7(links_r7)

export_csv(dados_g1,dados_uol,dados_r7)

time_elapsed = datetime.now() - start_time
print(f'Tempo total (hh:mm:ss.ms) {time_elapsed}')