import asyncio
import aiohttp
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


qntd_noticias = 10

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,en-US;q=0.7,en;q=0.3',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    'Priority': 'u=0, i',
}

sitemap_g1 = "https://g1.globo.com/rss/g1/educacao/"
sitemap_uol = "https://noticias.uol.com.br/sitemap/v2/today.xml"
sitemap_r7 = "https://www.r7.com/arc/outboundfeeds/sitemap/latest/"

async def get_sitemap(session, url):
    async with session.get(url, headers=headers) as response_sitemap:
        if response_sitemap.status != 200:
            print("Sitemap não carregado:", url)
            return None
        text = await response_sitemap.text()
        return BeautifulSoup(text, features="xml")


async def fetch_html(session, url):
    async with session.get(url, headers=headers) as response:
        return await response.text()


def get_dados_g1(all_itens_g1):
    links_g1 = []
    title_g1 = []
    subtitle_g1 = []
    date_iso_g1 = []

    for item in all_itens_g1[:qntd_noticias]:
        link = item.find('link')
        links_g1.append(link.text if link else None)

        title = item.find('title')
        title_g1.append(title.text if title else None)

        subtitle = item.find('atom:subtitle')
        subtitle_g1.append(subtitle.text if subtitle else title.text)

        data_tag = item.find('pubDate')
        if data_tag:
            dt = datetime.strptime(data_tag.text, "%a, %d %b %Y %H:%M:%S %z")
            date_iso_g1.append(dt.isoformat())
        else:
            date_iso_g1.append(None)

    return {
        "Veiculo": ["G1"] * len(links_g1),
        "Link da matéria": links_g1,
        "Título da Matéria": title_g1,
        "Subtítulo": subtitle_g1,
        "Data(ISO)": date_iso_g1,
    }


def get_itens_uol_r7(soup):
    return soup.find_all('url')


def get_links_uol_r7(all_itens):
    links = []
    for item in all_itens[:qntd_noticias]:
        loc = item.find('loc')
        links.append(loc.text if loc else None)
    return links


async def parse_single_uol(session, link):
    resp_text = await fetch_html(session, link)
    soup = BeautifulSoup(resp_text, "lxml")

    if "newsletters" in link:
        title_tag = soup.find("td", class_="title") or soup.find("h1", class_="headline")
        title = title_tag.text.strip() if title_tag else None

        subtitle_tag = soup.find("td", class_="manchete-texto")
        if subtitle_tag:
            p = subtitle_tag.find_all("p")
            subtitle = p[0].text.strip() if p else None
        else:
            subtitle = None

        date_tag = soup.find("time", class_="date")
        date_iso = date_tag["datetime"] if (date_tag and date_tag.has_attr("datetime")) else None

        return title, subtitle, date_iso

    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else None

    subtitle_tag = soup.find("meta", property="og:description")
    subtitle = subtitle_tag["content"].strip() if subtitle_tag else None

    date_tag = soup.find("time", class_="date")
    date_iso = date_tag["datetime"] if (date_tag and date_tag.has_attr("datetime")) else None

    return title, subtitle, date_iso


async def get_dados_uol(session, links):
    tasks = [parse_single_uol(session, link) for link in links]
    results = await asyncio.gather(*tasks)

    title_uol = []
    subtitle_uol = []
    date_iso_uol = []

    for title, subtitle, date_iso in results:
        title_uol.append(title)
        subtitle_uol.append(subtitle)
        date_iso_uol.append(date_iso)

    return {
        "Veiculo": ["Uol"] * len(links),
        "Link da matéria": links,
        "Título da Matéria": title_uol,
        "Subtítulo": subtitle_uol,
        "Data(ISO)": date_iso_uol,
    }


async def parse_single_r7(session, link):
    resp_text = await fetch_html(session, link)
    soup = BeautifulSoup(resp_text, "lxml")

    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else None

    subtitle_tag = soup.find("h2")
    subtitle = subtitle_tag.text.strip() if subtitle_tag else None

    date_tag = soup.find("time")
    date_iso = date_tag["datetime"] if (date_tag and date_tag.has_attr("datetime")) else None

    return title, subtitle, date_iso


async def get_dados_r7(session, links):
    tasks = [parse_single_r7(session, link) for link in links]
    results = await asyncio.gather(*tasks)

    title_r7 = []
    subtitle_r7 = []
    date_iso_r7 = []

    for title, subtitle, date_iso in results:
        title_r7.append(title)
        subtitle_r7.append(subtitle)
        date_iso_r7.append(date_iso)

    return {
        "Veiculo": ["R7"] * len(links),
        "Link da matéria": links,
        "Título da Matéria": title_r7,
        "Subtítulo": subtitle_r7,
        "Data(ISO)": date_iso_r7,
    }


def export_csv(d_g1, d_uol, d_r7):
    df = pd.concat([
        pd.DataFrame(d_g1),
        pd.DataFrame(d_uol),
        pd.DataFrame(d_r7)
    ], ignore_index=True)

    df.to_csv("result.csv", index=False, sep=";")


async def main():
    async with aiohttp.ClientSession() as session:
        
        # G1
        soup_g1 = await get_sitemap(session, sitemap_g1)
        all_itens_g1 = soup_g1.find_all('item')
        dados_g1 = get_dados_g1(all_itens_g1)

        # UOL
        soup_uol = await get_sitemap(session, sitemap_uol)
        all_itens_uol = get_itens_uol_r7(soup_uol)
        links_uol = get_links_uol_r7(all_itens_uol)
        dados_uol = await get_dados_uol(session, links_uol)

        # R7
        soup_r7 = await get_sitemap(session, sitemap_r7)
        all_items_r7 = get_itens_uol_r7(soup_r7)
        links_r7 = get_links_uol_r7(all_items_r7)
        dados_r7 = await get_dados_r7(session, links_r7)

        export_csv(dados_g1, dados_uol, dados_r7)

start_time = datetime.now()
asyncio.run(main())
time_elapsed = datetime.now() - start_time
print(f"Tempo total (hh:mm:ss.ms): {time_elapsed}")