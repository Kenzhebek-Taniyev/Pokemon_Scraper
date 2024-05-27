import unittest
import aiohttp
import asyncio
from unittest.mock import patch, AsyncMock
import scraper

class TestScraper(unittest.TestCase):

    @patch('scraper.aiohttp.ClientSession.get')
    def test_fetch_page(self, mock_get):
        url = "https://scrapeme.live/shop/"
        expected_content = "<html></html>"
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=expected_content)
        
        async def test_async():
            async with aiohttp.ClientSession() as session:
                content = await scraper.fetch_page(session, url)
                self.assertEqual(content, expected_content)

        asyncio.run(test_async())

    def test_parse_pokemon_list(self):
        content = """
        <li class="post-759 product type-product status-publish has-post-thumbnail product_cat-pokemon product_cat-seed product_tag-bulbasaur product_tag-overgrow product_tag-seed first instock sold-individually taxable shipping-taxable purchasable product-type-simple">
            <a href="https://scrapeme.live/shop/Bulbasaur/" class="woocommerce-LoopProduct-link woocommerce-loop-product__link"><img width="324" height="324" src="https://scrapeme.live/wp-content/uploads/2018/08/001-350x350.png" class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail wp-post-image" alt="" srcset="https://scrapeme.live/wp-content/uploads/2018/08/001-350x350.png 350w, https://scrapeme.live/wp-content/uploads/2018/08/001-150x150.png 150w, https://scrapeme.live/wp-content/uploads/2018/08/001-300x300.png 300w, https://scrapeme.live/wp-content/uploads/2018/08/001-100x100.png 100w, https://scrapeme.live/wp-content/uploads/2018/08/001-250x250.png 250w, https://scrapeme.live/wp-content/uploads/2018/08/001.png 475w" sizes="(max-width: 324px) 100vw, 324px"><h2 class="woocommerce-loop-product__title">Bulbasaur</h2>
            <span class="price"><span class="woocommerce-Price-amount amount"><span class="woocommerce-Price-currencySymbol">£</span>63.00</span></span>
        </a><a href="/shop/?add-to-cart=759" data-quantity="1" class="button product_type_simple add_to_cart_button ajax_add_to_cart" data-product_id="759" data-product_sku="4391" aria-label="Add “Bulbasaur” to your basket" rel="nofollow">Add to basket</a></li>
        """
        pokemons = scraper.parse_pokemon_list(content)
        self.assertEqual(len(pokemons), 1)
        self.assertEqual(pokemons[0]['name'], 'Bulbasaur')
        self.assertEqual(pokemons[0]['price'], '£63.00')
        self.assertEqual(pokemons[0]['sku'], '4391')
        self.assertEqual(pokemons[0]['image_url'], 'https://scrapeme.live/wp-content/uploads/2018/08/001-350x350.png')

    @patch('scraper.fetch_page')
    def test_get_all_pokemon(self, mock_fetch_page):
        pages = [
            """
            <li class="post-759 product type-product status-publish has-post-thumbnail product_cat-pokemon product_cat-seed product_tag-bulbasaur product_tag-overgrow product_tag-seed first instock sold-individually taxable shipping-taxable purchasable product-type-simple">
                <a href="https://scrapeme.live/shop/Bulbasaur/" class="woocommerce-LoopProduct-link woocommerce-loop-product__link"><img width="324" height="324" src="https://scrapeme.live/wp-content/uploads/2018/08/001-350x350.png" class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail wp-post-image" alt="" srcset="https://scrapeme.live/wp-content/uploads/2018/08/001-350x350.png 350w, https://scrapeme.live/wp-content/uploads/2018/08/001-150x150.png 150w, https://scrapeme.live/wp-content/uploads/2018/08/001-300x300.png 300w, https://scrapeme.live/wp-content/uploads/2018/08/001-100x100.png 100w, https://scrapeme.live/wp-content/uploads/2018/08/001-250x250.png 250w, https://scrapeme.live/wp-content/uploads/2018/08/001.png 475w" sizes="(max-width: 324px) 100vw, 324px"><h2 class="woocommerce-loop-product__title">Bulbasaur</h2>
                <span class="price"><span class="woocommerce-Price-amount amount"><span class="woocommerce-Price-currencySymbol">£</span>63.00</span></span>
            </a><a href="/shop/?add-to-cart=759" data-quantity="1" class="button product_type_simple add_to_cart_button ajax_add_to_cart" data-product_id="759" data-product_sku="4391" aria-label="Add “Bulbasaur” to your basket" rel="nofollow">Add to basket</a></li>
            """,
            """
            <li class="post-760 product type-product status-publish has-post-thumbnail product_cat-pokemon product_cat-seed product_tag-charmander product_tag-flame product_tag-seed first instock sold-individually taxable shipping-taxable purchasable product-type-simple">
                <a href="https://scrapeme.live/shop/Charmander/" class="woocommerce-LoopProduct-link woocommerce-loop-product__link"><img width="324" height="324" src="https://scrapeme.live/wp-content/uploads/2018/08/002-350x350.png" class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail wp-post-image" alt="" srcset="https://scrapeme.live/wp-content/uploads/2018/08/002-350x350.png 350w, https://scrapeme.live/wp-content/uploads/2018/08/002-150x150.png 150w, https://scrapeme.live/wp-content/uploads/2018/08/002-300x300.png 300w, https://scrapeme.live/wp-content/uploads/2018/08/002-100x100.png 100w, https://scrapeme.live/wp-content/uploads/2018/08/002-250x250.png 250w, https://scrapeme.live/wp-content/uploads/2018/08/002.png 475w" sizes="(max-width: 324px) 100vw, 324px"><h2 class="woocommerce-loop-product__title">Charmander</h2>
                <span class="price"><span class="woocommerce-Price-amount amount"><span class="woocommerce-Price-currencySymbol">£</span>45.00</span></span>
            </a><a href="/shop/?add-to-cart=760" data-quantity="1" class="button product_type_simple add_to_cart_button ajax_add_to_cart" data-product_id="760" data-product_sku="4392" aria-label="Add “Charmander” to your basket" rel="nofollow">Add to basket</a></li>
            """
        ]
        mock_fetch_page.side_effect = pages + [aiohttp.ClientResponseError(None, (), status=404)]

        async def test_async():
            pokemons = await scraper.get_all_pokemon()
            self.assertEqual(len(pokemons), 2)
            self.assertEqual(pokemons[0]['name'], 'Bulbasaur')
            self.assertEqual(pokemons[1]['name'], 'Charmander')

        asyncio.run(test_async())

if __name__ == '__main__':
    unittest.main()
