import os
import urllib.request as requests
import re

urls_regex = re.compile(
    r"(https:\/\/[^cdn\.][a-z0-9\-]+.cyberdrop.to\/[a-z0-9_\-A-Z]+.(jpg|png|mp4|mkv|avi|jpeg|gif|webm|webp|wmv|mov))")


def export_from(short_code: str, asynchronous: bool=False) -> list:
    assert isinstance(
        short_code, str), "The 'short_code' has to be of type string and must represents the resource's endpoint."

    url = "https://cyberdrop.me/a/" + short_code
    print(url)
    http = requests.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with requests.urlopen(http) as response:
        html = response.read().decode("utf-8")
    response.close()
    regexed_urls = urls_regex.findall(html)

    urls = []
    for match in regexed_urls:
        url = match[0]
        if url not in urls:
            if asynchronous:
                yield url
            else:
                urls.append(url)

    if not asynchronous:
        return urls


def is_video(url: str):
    return url[-3:] in ("mp4", "mkv", "mov")


def downloader(url: str, output: str, skip_video: bool = False):
    if skip_video and is_video(url): return

    http = requests.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = requests.urlopen(http).read()

    if len(data) <= 0: return

    filename = url.split('/')[-1].split('?')[0]
    if filename in os.listdir(output): return

    with open(os.path.join(output, filename), 'wb+') as s:
        s.write(data)
    s.close()
