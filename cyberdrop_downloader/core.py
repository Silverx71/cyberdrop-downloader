import os
import re
import urllib.request as requests

urls_regex = re.compile(
    r"https:\/\/[^cdn\.][a-z0-9\-]+.cyberdrop.to\/[a-z0-9_\-A-Z]+.(?:mp4|mov|m4v|ts|mkv|avi|wmv|webm|vob|gifv|mpg|mpeg|mp3|flac|wav|png|jpeg|jpg|gif|bmp|webp|heif|heic|tiff|svf|svg|ico|psd|ai|pdf|txt|log|csv|xml|cbr|zip|rar|7z|tar|gz|xz|targz|tarxz|iso|torrent|kdbx)")


def export_from(short_code: str, asynchronous: bool=False) -> list:
    assert isinstance(
        short_code, str), "The 'short_code' has to be of type string and must represents the resource's endpoint."

    http = requests.Request("https://cyberdrop.me/a/" + short_code, headers={"User-Agent": "Mozilla/5.0"})
    response = requests.urlopen(http)
    html = response.read().decode("utf-8")
    response.close()

    regexed_urls = urls_regex.findall(html)

    urls = []
    for url in regexed_urls:
        if url in urls: continue
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
    response = requests.urlopen(http)
    data = response.read()
    response.close()

    if len(data) <= 0: return

    filename = url.split('/')[-1].split('?')[0]
    if filename in os.listdir(output): return

    with open(os.path.join(output, filename), 'wb+') as s:
        s.write(data)
    s.close()
