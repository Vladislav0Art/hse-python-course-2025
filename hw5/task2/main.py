#!/usr/bin/env python3
import argparse
import asyncio
import logging
import os
import json
from dataclasses import dataclass
from typing import Union

from bs4 import BeautifulSoup
from pathlib import Path

import aiofiles
import aiohttp

from hw5.utils import create_artifacts_dir, prepare_logger


@dataclass
class Recommendation:
    link: str | None = None
    price_rub: str | None = None
    apartment_info: str | None = None
    apartment_address: str | None = None


async def save_file(path: Path, recommendations: list[Recommendation]):
    async with aiofiles.open(path, 'w', encoding='utf-8') as f:
        json_rec = json.dumps([rec.__dict__ for rec in recommendations], indent=4, ensure_ascii=False)
        await f.write(json_rec)


async def parse_recommendation(logger, recommendation, i: int) -> Union[Recommendation, None]:
    logger.info(f"Parsing recommendation {i}")
    link_area = recommendation.find('div', {'data-name': 'LinkArea'})
    if link_area is None:
        return None
    price_div = link_area.find('div')
    price = price_div.find('span').text.strip() if price_div is not None and price_div.find('span') else None
    info = None
    links = link_area.find_all('a')
    if len(links) > 1:
        info = links[1].text.strip()
    address = None
    divs = link_area.find_all('div')
    last_div = divs[-1]
    if last_div.find('span'):
        address = last_div.find('span').text.strip()

    return Recommendation(
        link=link_area.find('a')['href'],
        price_rub=price,
        apartment_info=info,
        apartment_address=address
    )


async def scrap_info(logger: logging.Logger, num_recommendations: int, save_path: Path) -> None:
    url = "https://www.cian.ru/recommendations/"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text(encoding='utf-8')
                    soup = BeautifulSoup(data, 'html.parser')
                    recommendations = soup.find_all('div', {'data-name': 'RecommendationsContainer'})
                    tasks = [
                        parse_recommendation(logger, recommendation, i)
                        for i, recommendation in enumerate(recommendations[:num_recommendations])
                    ]
                    results = (await asyncio.gather(*tasks))
                    answer = [rec for rec in results if rec is not None]

                    await save_file(save_path, answer)
                    logger.info(f"Downloaded {num_recommendations} recommendations into {save_path}")
                else:
                    logger.error(f"Failed to extract data from '{url}': {response.status}, {await response.text()}")
        except Exception as e:
            logger.error(f"Error extracting data: {e}")



def main(logger: logging.Logger):
    parser = argparse.ArgumentParser(description='Download recommendations from cian asynchronously')
    parser.add_argument('-n', '--num_recommendations', type=int, required=True, default=1, help='Number of recommendations to scrap')
    parser.add_argument('-f', '--dirpath', type=str, required=True, help='Directory where images will be saved')

    args = parser.parse_args()
    logger.info(f"Downloading {args.num_recommendations} recommendations into {args.dirpath}")

    num_recommendations = args.num_recommendations

    dirpath = Path(args.dirpath)
    dirpath.mkdir(parents=True, exist_ok=True)
    save_path = dirpath / "result.json"
    # start scrapping
    asyncio.run(scrap_info(logger, num_recommendations, save_path))



if __name__ == "__main__":
    # example: `python -m hw5.task2.main -n 5 -f hw5/artifacts/task2/recommendations`
    artifacts_dir = create_artifacts_dir(dirname="task2")
    log_filepath = os.path.join(artifacts_dir, "execution.log")

    logger = prepare_logger(logger_name="cian-scraping", filepath=log_filepath)
    main(logger)