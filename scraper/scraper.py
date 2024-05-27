import aiohttp
import asyncio
from bs4 import BeautifulSoup

BASE_URL = "https://scrapeme.live/shop/"

async def fetch_page(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()

def parse_pokemon_list(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    pokemons = []
    seen_skus = set()

    for item in soup.select('li.product'):
        product_id = item['class'][0].split('-')[-1]
        name = item.select_one('h2.woocommerce-loop-product__title').text
        price = item.select_one('span.price').text.strip()
        sku = item.select_one('a.add_to_cart_button')['data-product_sku']
        image_url = item.select_one('img')['src']

        if sku not in seen_skus:
            seen_skus.add(sku)
            pokemons.append({
                "id": int(product_id),
                "name": name,
                "price": price,
                "sku": sku,
                "image_url": image_url
            })

    return pokemons

async def get_all_pokemon():
    async with aiohttp.ClientSession() as session:
        page_num = 1
        pokemons = []
        while True:
            url = f"{BASE_URL}page/{page_num}/"
            try:
                page_content = await fetch_page(session, url)
                new_pokemons = parse_pokemon_list(page_content)
                if not new_pokemons:
                    break
                pokemons.extend(new_pokemons)
                page_num += 1
            except aiohttp.ClientResponseError as e:
                if e.status == 404:
                    break
                else:
                    raise
        return pokemons
