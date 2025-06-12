
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

def scrape_walmart(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector('[data-testid^="product-tile"]')  # Esperamos productos

        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    items = soup.select('[data-testid^="product-tile"]')

    data = []

    for item in items:
        # Nombre y enlace
        try:
            nombre_tag = item.find('span', attrs={'data-automation-id': 'product-title'})
            nombre = nombre_tag.get_text(strip=True)
            link = item.select_one("a")["href"]
            if not link.startswith("http"):
                link = "https://www.walmart.com.mx" + link
        except:
            nombre = link = ""

        # Marca
        try:
            marca = item.select_one("div.mt2.mb1.b.f6.black.mr1.lh-copy").get_text(strip=True)
        except:
            marca = ""

        # Precio actual
        try:
            precio_tag = item.select_one("div.b.black.green")


            if not precio_tag:
                precio_tag = item.select_one("div.b.black.lh-copy")

            
            if precio_tag:
                precio_actual = precio_tag.get_text(strip=True)
            else:
                precio_actual = ""
        except:
            precio_actual = ""

        # Precio anterior
        try:
            precio_anterior = item.select_one("div.strike").get_text(strip=True)
        except:
            precio_anterior = ""

        # Ahorro
        try:
            ahorro = item.select_one("div.bg-washed-green span").get_text(strip=True)
        except:
            ahorro = ""

        # Imagen
        try:
            img_tag = item.select_one("img")
            imagen_url = img_tag.get("srcset", "").split(" ")[0] or img_tag.get("src", "")
        except:
            imagen_url = ""

        data.append({
            "Nombre del producto": nombre,
            "Marca": marca,
            "Precio actual": precio_actual,
            "Precio anterior": precio_anterior,
            "Descuento": ahorro,
            "Imagen URL": imagen_url,
            "Link al producto": link,
            "Nombre del sitio": "Walmart",
        })

    df = pd.DataFrame(data)
    return df

# Ejecutar
url = "https://www.walmart.com.mx/content/celulares/264800?q=celulares"
df = scrape_walmart(url)
print(df.head())
df.to_csv("walmart_celulares.csv", index=False)