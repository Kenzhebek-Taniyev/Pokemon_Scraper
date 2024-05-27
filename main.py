import asyncio
from scraper.scraper import get_all_pokemon
from scraper.utils import save_to_json

def main():
    pokemons = asyncio.run(get_all_pokemon())
    save_to_json(pokemons, 'result.json')

if __name__ == "__main__":
    main()
