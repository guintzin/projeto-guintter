# %% g1
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

qntd_noticias = 70

sitemap_g1 = "https://g1.globo.com/rss/g1/educacao/"
cookies = {
    'cookie-banner-consent-accepted': 'false',
    '_pctx': '%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIEYOBWAJh44A2QQAYRADgAsggMyjJAdhABfIA',
    '_pcid': '%7B%22browserId%22%3A%22meafp4orhseb2viq%22%7D',
    'xbc': '%7Bkpex%7DL1JHFU6Xo4Mf-C8rYQ0XsW7uxbHEJIFRdmq6z6kwVV5nA4Cxu_5BYPlgaj6lrpv_wJiM8o6LzB7Xjlgiqdh-Dz7C0F8TiZ7i1QizdOl5GGwF9vdQHFPzLHwV6cw0SnmUewBZ840yNKc-z1AEedzEDm-gZc1vM82KCWeim2wVcN2-hJklVgOACAFGCFF-5h_yrJWw4PaSfAI7-H1FeET8dj84vVlS8D5MbPOzgSXLNlUmTEprjZ8Tom0pBtWgjxUdKDTy5pNbRwBSyhmk0U-6jeIpQ0UUfWswXGq08eZ_iKT6p_7uhWOVLShF5Zsyt1BceCRl7Mn_EDnBScJlmF8WYw',
    '_pcus': 'eyJ1c2VyU2VnbWVudHMiOnsiQ09NUE9TRVIxWCI6eyJzZWdtZW50cyI6WyJMVHM6ODNmZDM5NjNlMzg3M2NkYjZiMDg3MjBkNWNkZGYwODk5OTgxZGUxMDpub19zY29yZSJdfX19',
    '_pc_randomCookieForPiano': 'cookieB',
    '__pat': '-10800000',
    '__tbc': '%7Bkpex%7DUdmkXHS-TIPju1QycNOmMJTI8CyOPaPeZR8ZGRb88NnOfe97V6sqLXT1dCNQV9W9',
    'glb_uid': '"S_gxUipRQs3jMNxXQp8kWFvfT1weWtv3McUpaPxMXIM="',
    '_ga': '1.1',
    'glbExpIdToken': '',
}
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
 
resp_site_map_g1 = requests.get(sitemap_g1, cookies=cookies, headers=headers)
soup_g1 = BeautifulSoup(resp_site_map_g1._content, "xml")
all_items_g1 = soup_g1.find_all('item')

links_g1 = []
title_g1 = []
subtitle_g1 = []
date_iso_g1 =[]

for item in all_items_g1 [:qntd_noticias]:

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
        subtitle_g1.append(None)

    data_tag = item.find('pubDate')
    if data_tag:
        data_tag = data_tag.text
        dt = datetime.strptime(data_tag,"%a, %d %b %Y %H:%M:%S %z")
        data_tag = dt.isoformat()
        date_iso_g1.append(data_tag)
    else:
        date_iso_g1.append(None)

data_g1={
    "Veiculo":["G1"] * len(links_g1),
    "Link da matéria" : links_g1,
    "Título da Matéria" : title_g1,
    "Subtítulo" : subtitle_g1,
    "Data(ISO)" : date_iso_g1,
    }

df_g1 = pd.DataFrame(data_g1)
df_g1.to_csv("result.csv", index=False, sep = ";")

#  uol
sitemap_uol = "https://noticias.uol.com.br/sitemap/v2/today.xml"
cookies = {
    '_pctx': '%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIEYOBmAdgBZeATiEcADLwBMkjpO5iAbBxABfIA',
    'TRINITY_USER_DATA': 'eyJ1c2VySWRUUyI6MTc1NDM2MzEwOTczNn0=',
    'TRINITY_USER_ID': 'eb11b302-e477-440f-b534-855ac46278a8',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,en-US;q=0.7,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Connection': 'keep-alive',
    # 'Cookie': '_pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIEYOBmAdgBZeATiEcADLwBMkjpO5iAbBxABfIA; TRINITY_USER_DATA=eyJ1c2VySWRUUyI6MTc1NDM2MzEwOTczNn0=; TRINITY_USER_ID=eb11b302-e477-440f-b534-855ac46278a8',
    'Priority': 'u=0, i',
}

resp_site_map_uol = requests.get(sitemap_uol, cookies=cookies, headers=headers)
soup_uol = BeautifulSoup(resp_site_map_uol._content, "xml")
all_items_uol = soup_uol.find_all('url')

links_uol = []
title_uol = []
subtitle_uol = []
date_iso_uol =[]

for item in all_items_uol[:qntd_noticias]:
    link_tag = item.find('loc')
    if link_tag:
        links_uol.append(link_tag.text)
    else:
        links_uol.append(None)
        
for link in links_uol[:qntd_noticias]:
    resp_inside_uol = requests.get(link, headers=headers, cookies=cookies)  
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

data_uol={
    "Veiculo" : ["Uol"] * len(links_uol ),
    "Link da matéria" : links_uol,
    "Título da Matéria" : title_uol,
    "Subtítulo" : subtitle_uol,
    "Data(ISO)" : date_iso_uol,
    }

df_uol = pd.DataFrame(data_uol)
df_uol.to_csv("result.csv", index=False, sep=";", mode="a", header=False)

# R7
sitemap_r7 = "https://www.r7.com/arc/outboundfeeds/sitemap/latest/"
cookies = {
    'r7_lgpd_accepted': 'true',
    '_gcl_au': '1.1.2038652605.1758227677',
    '_scor_uid': '72a613f9c30a4455a7e595c856ae279d',
    '_cb': 'BEs0TaCDrgbGCXvFg4',
    '_chartbeat2': '.1758227677341.1758324667653.11.sqknQBPHPyvDqh6qNB7e5mHqcrXo.1',
    'permutive-id': '2d8c5bf4-31c8-4f95-911b-7adc88bfba99',
    '_ga_JEN7KT287N': 'GS2.1.s1758324668$o7$g0$t1758324725$j3$l0$h0',
    '_ga': 'GA1.1.695007993.1758227678',
    'RT': '"z=1&dm=www.r7.com&si=dfb41aaf-5f48-43a6-bcf4-d3bc8cb64ccb&ss=mfrh3u8n&sl=1&tt=anm&rl=1&ld=ann&ul=1b28&hd=1b6l"',
    '_v__chartbeat3': 'N2m4UDxfyFi-JzeL',
    '_cc_id': '3fe5364eab258fbec8273efdf1766018',
    '__gads': 'ID=e166d598c334e359:T=1758227682:RT=1758324668:S=ALNI_MZNsMDMz3PnXNK4EL4nawL6-dWRig',
    '__gpi': 'UID=0000128e51f1f2e0:T=1758227682:RT=1758324668:S=ALNI_MayqdROJ5ARhZ8057KVmuf0nybXbA',
    '__eoi': 'ID=aec16fd7c8a7fb60:T=1758227682:RT=1758324668:S=AA-AfjbG0LIo2qBr7belKe63sPwj',
    '__qca': 'P1-ed802b57-c7b2-4327-995e-f3aa2bc26a06',
    'cto_bundle': 'F21dgF9aZmlCck9mVzRrRHFGdmJLbFBNZGdkYSUyQkNDRGNSWiUyQlNkeEVtQ29IJTJCekt4NjNidXIzVzhKSjd1Zm14R01Yc2FXY2NmdFgzSlFDVjFybkM5TFFuV2JpUzBDSEVTV3dNaXFCTiUyRkdyU0NsZ1prQjF6cjE4bHoxZWFmYWdzM1AwYXAlMkZCRndiYUJianFqWFJnMGtDUWZqdWl0enRwdlg5MzRvWGtKcXRGUiUyQlpac1klM0Q',
    '_ttuu.s': '1758324678936',
    'tt.u': '0100007FFD6CCC686C06236B02AD1E03',
    '_pbjs_userid_consent_data': '3524755945110770',
    'cto_bidid': '6p_8TV9ubHlqYU5ZcDI4MXR3N2NPWk1nSGNuVDhLbHBhOVF1QjRmZndUZmkwckhCRjZpWGtGb0tGamEydnJGRzRhekQlMkJEdnhkOTBUMTE5cEl6bCUyQlBXcmtLZCUyRlZmcmlhWElKVzVoVDRNcWtlTyUyRkZjNTd3R29lMDBtQWh6dnZkeUFxR044',
    'cto_dna_bundle': 'HfF_il9aZmlCck9mVzRrRHFGdmJLbFBNZGdVcFRqc2xDZERFenpYOHVZOTVPM05sU0NRQnBLZXZFUXE1aDZidiUyRiUyQmtnWGVJU1M0TURxR1d1VXZnd1N6bVYyQ2clM0QlM0Q',
    'tt.nprf': '',
    'AKA_A2': 'A',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,en-US;q=0.7,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Connection': 'keep-alive',
    # 'Cookie': 'r7_lgpd_accepted=true; _gcl_au=1.1.2038652605.1758227677; _scor_uid=72a613f9c30a4455a7e595c856ae279d; _cb=BEs0TaCDrgbGCXvFg4; _chartbeat2=.1758227677341.1758324667653.11.sqknQBPHPyvDqh6qNB7e5mHqcrXo.1; permutive-id=2d8c5bf4-31c8-4f95-911b-7adc88bfba99; _ga_JEN7KT287N=GS2.1.s1758324668$o7$g0$t1758324725$j3$l0$h0; _ga=GA1.1.695007993.1758227678; RT="z=1&dm=www.r7.com&si=dfb41aaf-5f48-43a6-bcf4-d3bc8cb64ccb&ss=mfrh3u8n&sl=1&tt=anm&rl=1&ld=ann&ul=1b28&hd=1b6l"; _v__chartbeat3=N2m4UDxfyFi-JzeL; _cc_id=3fe5364eab258fbec8273efdf1766018; __gads=ID=e166d598c334e359:T=1758227682:RT=1758324668:S=ALNI_MZNsMDMz3PnXNK4EL4nawL6-dWRig; __gpi=UID=0000128e51f1f2e0:T=1758227682:RT=1758324668:S=ALNI_MayqdROJ5ARhZ8057KVmuf0nybXbA; __eoi=ID=aec16fd7c8a7fb60:T=1758227682:RT=1758324668:S=AA-AfjbG0LIo2qBr7belKe63sPwj; __qca=P1-ed802b57-c7b2-4327-995e-f3aa2bc26a06; cto_bundle=F21dgF9aZmlCck9mVzRrRHFGdmJLbFBNZGdkYSUyQkNDRGNSWiUyQlNkeEVtQ29IJTJCekt4NjNidXIzVzhKSjd1Zm14R01Yc2FXY2NmdFgzSlFDVjFybkM5TFFuV2JpUzBDSEVTV3dNaXFCTiUyRkdyU0NsZ1prQjF6cjE4bHoxZWFmYWdzM1AwYXAlMkZCRndiYUJianFqWFJnMGtDUWZqdWl0enRwdlg5MzRvWGtKcXRGUiUyQlpac1klM0Q; _ttuu.s=1758324678936; tt.u=0100007FFD6CCC686C06236B02AD1E03; _pbjs_userid_consent_data=3524755945110770; cto_bidid=6p_8TV9ubHlqYU5ZcDI4MXR3N2NPWk1nSGNuVDhLbHBhOVF1QjRmZndUZmkwckhCRjZpWGtGb0tGamEydnJGRzRhekQlMkJEdnhkOTBUMTE5cEl6bCUyQlBXcmtLZCUyRlZmcmlhWElKVzVoVDRNcWtlTyUyRkZjNTd3R29lMDBtQWh6dnZkeUFxR044; cto_dna_bundle=HfF_il9aZmlCck9mVzRrRHFGdmJLbFBNZGdVcFRqc2xDZERFenpYOHVZOTVPM05sU0NRQnBLZXZFUXE1aDZidiUyRiUyQmtnWGVJU1M0TURxR1d1VXZnd1N6bVYyQ2clM0QlM0Q; tt.nprf=; AKA_A2=A',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'If-Modified-Since': 'Sat, 20 Sep 2025 02:00:36 GMT',
    'If-None-Match': 'W/"467f-FRPYwoykjPRMMeJLjRO3axpQ0JE"',
    'Priority': 'u=0, i',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

resp_site_map_r7 = requests.get(sitemap_r7, cookies=cookies, headers=headers)
soup_r7 = BeautifulSoup(resp_site_map_r7._content, "xml")
all_items_r7 = soup_r7.find_all('url')

links_r7 = []
title_r7 = []
subtitle_r7 = []
date_iso_r7 =[]

for item in all_items_r7[:qntd_noticias]:
    link_tag = item.find('loc')
    if link_tag:
        links_r7.append(link_tag.text)
    else:
        links_r7.append(None)

for link in links_r7[:qntd_noticias]:
    resp_inside_r7 = requests.get(link, headers=headers, cookies=cookies) 
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

df_r7 = pd.DataFrame(data_r7)
df_r7.to_csv("result.csv", index=False, sep=";", mode="a", header=False)