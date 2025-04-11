#!/usr/bin/env python3
import asyncio
import logging
import os
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


async def save_file(path: Path, data):
    async with aiofiles.open(path, 'wb') as f:
        await f.write(data)

async def parse_recommendation(recommendation) -> Union[Recommendation, None]:
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
    save_path.mkdir(parents=True, exist_ok=True)
    url = "https://www.cian.ru/recommendations/"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text(encoding='utf-8')
                    soup = BeautifulSoup(data, 'html.parser')
                    answer = []
                    recommendations = soup.find_all('div', {'data-name': 'RecommendationsContainer'})

                    for recommendation in recommendations:
                        if len(answer) >= num_recommendations:
                            break
                        rec: Union[Recommendation, None] = await parse_recommendation(recommendation)
                        if rec is not None:
                            answer.append(rec)

                    print(answer)
                    # await save_file(image_path, image_data)
                    # logger.info(f"Downloaded image {image_id} to {image_path}")
                else:
                    logger.error(f"Failed to extract data from '{url}': {response.status}, {await response.text()}")
        except Exception as e:
            logger.error(f"Error extracting data: {e}")



def main(logger: logging.Logger):
    num_recommendations = 10
    # TODO: replace
    filepath = "/Users/vartiukhov/dev/studies/hse/2025/python/hw5/artifacts/task2/images"
    save_path = Path(filepath)
    # start scrapping
    asyncio.run(scrap_info(logger, num_recommendations, save_path))

if __name__ == "__main__":
    # example: `python -m hw5.task2.main`
    artifacts_dir = create_artifacts_dir(dirname="task1")
    log_filepath = os.path.join(artifacts_dir, "execution.log")

    logger = prepare_logger(logger_name="fibonacci", filepath=log_filepath)
    main(logger)