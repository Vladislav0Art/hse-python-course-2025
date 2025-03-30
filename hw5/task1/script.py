#!/usr/bin/env python3
import argparse
import asyncio
import logging

import aiohttp
import os
from pathlib import Path

from hw5.utils import prepare_logger
from hw5.utils import create_artifacts_dir


async def download_image(logger: logging.Logger, session: aiohttp.ClientSession, image_id: int, save_path: Path) -> None:
    """
    download a single image from `picsum.photos` website and save it to specified path
    Args:
        session: aiohttp client session
        image_id: identifier for image
        save_path: path where image will be saved
    """
    # image size 800x600
    url = f"https://picsum.photos/800/600"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()
                # save in file
                image_path = save_path / f"image_{image_id}.jpg"
                with open(image_path, 'wb') as f:
                    f.write(image_data)
                logger.info(f"Downloaded image {image_id} to {image_path}")
            else:
                logger.error(f"Failed to download image {image_id}. Status code: {response.status}")
    except Exception as e:
        logger.error(f"Error downloading image {image_id}: {e}")


async def download_images(logger: logging.Logger, num_images: int, save_path: Path) -> None:
    """
    download multiple images asynchronously
    Args:
        num_images: number of images to download
        save_path: directory where images will be saved
    """
    save_path.mkdir(parents=True, exist_ok=True)
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_image(logger, session, i, save_path)
            for i in range(num_images)
        ]
        # execute all requests
        await asyncio.gather(*tasks)
    logger.info(f"Successfully downloaded {num_images} images to {save_path}")


def main(logger: logging.Logger):
    """
    CLI utility script that parses arguments and starts downloading process
    """
    parser = argparse.ArgumentParser(description='Download images from picsum.photos asynchronously')
    parser.add_argument('-n', '--num_images', type=int, required=True, help='Number of images to download')
    parser.add_argument('-f', '--filepath', type=str, required=True, help='Directory where images will be saved')

    args = parser.parse_args()
    logger.info(f"Downloading {args.num_images} images to {args.filepath}")
    
    save_path = Path(args.filepath)
    # start download
    asyncio.run(download_images(logger, args.num_images, save_path))


if __name__ == "__main__":
    # example: `python -m hw5.task1.script -n 5 -f hw5/artifacts/task1/images`
    artifacts_dir = create_artifacts_dir(dirname="task1")
    log_filepath = os.path.join(artifacts_dir, "execution.log")

    logger = prepare_logger(logger_name="fibonacci", filepath=log_filepath)
    main(logger)
