from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

def scrape_mercadolibre(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector('.poly-card')

        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    items = soup.select(".poly-card")

    data = []

    for item in items:
        try:
            nombre_tag = item.select_one("a.poly-component__title")
            nombre = nombre_tag.get_text(strip=True)
            link = nombre_tag["href"]
        except:
            nombre = link = ""

        try:
            marca = item.select_one("span.poly-component__brand").get_text(strip=True)
        except:
            marca = ""

        try:
            precio_actual = item.select_one("div.poly-price__current span.andes-money-amount__fraction").get_text(strip=True)
        except:
            precio_actual = ""

        try:
            precio_anterior = item.select_one("s span.andes-money-amount__fraction").get_text(strip=True)
        except:
            precio_anterior = ""

        try:
            descuento = item.select_one("span.andes-money-amount__discount").get_text(strip=True)
        except:
            descuento = ""

        try:
            imagen_element = item.select_one("div.poly-card__portada img")
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
            "Nombre del sitio": "Mercado Libre",
        })

    df = pd.DataFrame(data)
    return df

# Ejecutar
#url = "https://listado.mercadolibre.com.mx/celulares?sb=all_mercadolibre#D[A:celulares]"
url = "https://listado.mercadolibre.com.mx/celulares-telefonia/celulares-smartphones/celulares_Desde_51_NoIndex_True?sb=all_mercadolibre"
df = scrape_mercadolibre(url)
print(df.head())
df.to_csv("mercado_libre_pag2.csv", index=False)

