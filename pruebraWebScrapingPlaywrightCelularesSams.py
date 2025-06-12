from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

def scrape_sams(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector('div[role="group"][data-item-id]')

        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    items = soup.select('div[role="group"][data-item-id]')

    data = []

    for item in items:
        try:
            nombre_tag = item.select_one("span[data-automation-id='product-title']")
            nombre = nombre_tag.get_text(strip=True)
            link = item.select_one("a")["href"]
            if not link.startswith("http"):
                link = "https://www.sams.com.mx" + link
        except:
            nombre = link = ""

        try:
            marca = item.select_one("div.mb1.mt2.b.f6.black.mr1.lh-copy").get_text(strip=True)
        except:
            marca = ""

        try:
            precio_tag = item.select_one("div.mr1.mr2-xl.b.black.green")


            if not precio_tag:
                precio_tag = item.select_one("div.mr1.mr2-xl.b.black.lh-copy")

            
            if precio_tag:
                precio_actual = precio_tag.get_text(strip=True)
            else:
                precio_actual = ""
        except:
            precio_actual = ""

        try:
            precio_anterior = item.select_one("div.gray.mr1.strike.f7.f6-l").get_text(strip=True)
        except:
            precio_anterior = ""

        try:
            descuento = item.select_one("span.b.tc.green").get_text(strip=True)
        except:
            descuento = ""

        try:
            imagen_element = item.select_one("img[data-testid='productTileImage']")
            imagen_url = imagen_element.get("data-src") or imagen_element.get("src") or ""
        except:
            imagen_url = ""

        data.append({
            "Nombre del producto": nombre,
            "Marca": marca,
            "Precio actual": precio_actual,
            "Precio anterior": precio_anterior,
            "Descuento": descuento,
            "Imagen URL": imagen_url,
            "Link al producto": link,
            "Nombre del sitio": "Sams",
        })

    df = pd.DataFrame(data)
    return df

# Ejecutar
url = "https://www.sams.com.mx/search?q=celulares"
df = scrape_sams(url)
print(df.head())
df.to_csv("sams_celulares.csv", index=False)
