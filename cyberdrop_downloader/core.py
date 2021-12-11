import os
import re
import http.client as http_client
import urllib.request as requests
import urllib.error as requests_error

urls_regex = re.compile(
    r"(?:https:\/\/)[^cdn\.][a-z0-9\-\/\.]+.cyberdrop.(?:to|me)\/[a-z0-9_\-A-Z \(\)\/]+.(?:mp4|mov|m4v|ts|mkv|avi|wmv|webm|vob|gifv|mpg|mpeg|mp3|flac|wav|png|jpeg|jpg|gif|bmp|webp|heif|heic|tiff|svf|svg|ico|psd|ai|pdf|txt|log|csv|xml|cbr|zip|rar|7z|tar|gz|xz|targz|tarxz|iso|torrent|kdbx)")


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
        url = url.replace(" ", "%20")
        if "/thumbs/" in url: continue
        if "/s/" in url: continue
        if url.index("cyberdrop") < 14 or url.index("cyberdrop") > 18: continue
        if url in urls: continue
        if asynchronous:
            yield url
        else:
            urls.append(url)

    if not asynchronous:
        return urls


def is_video(url: str) -> bool:
    for e in ("mp4", "mov", "m4v", "ts", "mkv", "avi", "wmv", "webm", "vob", "gifv", "mpg", "mpeg"):
        if url.endswith(e):
            return True
    return False


def downloader(url: str, output: str, skip_video: bool = False):
    if skip_video and is_video(url): return

    filename = url.split('/')[-1].split('?')[0]
    filename = filename.replace("%20", ' ')
    if filename in os.listdir(output): return

    data = None


    try:
        requests.urlretrieve(url, os.path.join(output, filename))
        return
    except requests_error.ContentTooShortError:
        http = requests.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = requests.urlopen(http)
        data = response.read()
        while True:
            try:
                d = response.read(len(data))
            except http_client.IncompleteRead as e:
                data += e.partial
                continue
            else:
                data += d
                break
        response.close()
    except requests_error.HTTPError:
        return

    with open(os.path.join(output, filename), "wb+") as s:
        s.write(data)
    s.close()