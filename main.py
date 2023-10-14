import asyncio
import httpx
import tqdm
import json
import os
from cli import CommandLineParser

args = CommandLineParser.create_parser().parse_args()
cmd_args = CommandLineParser(**vars(args))

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        loaded_urls = json.load(file)
    return loaded_urls


async def download_files(url: str, filename: str, save_path: str):
    full_save_path = os.path.join(save_path, filename)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    with open(full_save_path, 'wb') as f:
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', url) as r:
                
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))

                tqdm_params = {
                    'desc': url,
                    'total': total,
                    'miniters': 1,
                    'unit': 'it',
                    'unit_scale': True,
                    'unit_divisor': 1024,
                }

                with tqdm.tqdm(**tqdm_params) as pb:
                    async for chunk in r.aiter_bytes():
                        pb.update(len(chunk))
                        f.write(chunk)


async def main():
    loop = asyncio.get_running_loop()

    urls = read_json_file(cmd_args.urls_file_path)

    tasks = [loop.create_task(download_files(url, filename, cmd_args.save_dir)) for url, filename in urls]
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())