import os
from multiprocessing.pool import ThreadPool
from typing import List
from urllib.parse import urlparse

import requests


def download_file(url: str, dest_filepath: str) -> str:
    print("- downloading", url)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return dest_filepath


def download_file_to_dir(url: str, dest_dirpath: str) -> str:
    filename = url.split("/")[-1]
    dest_file_path = f"{dest_dirpath}/{filename}"
    return download_file(url, dest_file_path)


def download_files_to_dir(urls: List[str], dest_dirpath: str):
    for url in urls:
        download_file_to_dir(url, dest_dirpath)


def download_files_to_dir_in_parallel(urls: List[str], dest_dirpath: str):
    urls_per_host = group_urls_by_host(urls)
    host_count = len(urls_per_host.keys())
    max_processes = os.cpu_count() - 1
    process_count = min(max_processes, host_count)

    pool = ThreadPool(processes=process_count)
    args = [(urls, dest_dirpath) for urls in urls_per_host.values()]
    pool.starmap_async(
        download_files_to_dir,
        args,
    )
    pool.close()
    pool.join()


def group_urls_by_host(urls: List[str]) -> dict[str, List[str]]:
    result = {}

    for url in urls:
        host = urlparse(url).netloc

        if host not in result:
            result[host] = []

        result[host].append(url)

    return result
