import os
import json
from cyberdrop_downloader import downloader, export_from


def prepare_folders(username: str):
    meta_filename = "meta.json"
    output = "downloads/"

    if not os.path.exists(output):
        os.mkdir(output)

    output = os.path.join(output, username)

    if not os.path.exists(output):
        os.mkdir(output)

    if meta_filename not in os.listdir(output):
        s = open(os.path.join(output, meta_filename), 'a')
        json.dump([], s)
        s.close()

    return meta_filename, output


def main(username: str, short_code: str = None, download: bool = False):
    # Prepares the output folders with the 'meta.json' file.
    meta_filename, output = prepare_folders(username)

    knowned_data: list = json.load(open(os.path.join(output, meta_filename)))

    if short_code:
        knowned_data.extend([url for url in export_from(
            short_code, asynchronous=True) if url not in knowned_data])

    # Saves the meta data :
    json.dump(knowned_data, open(os.path.join(output, meta_filename), "w+"))

    if download:
        files_output = os.path.join(output, "files")
        if not os.path.exists(files_output):
            os.mkdir(files_output)

        for url in knowned_data:
            downloader(url, files_output, False)


if __name__ == "__main__":
    main(username="bby_gee", short_code="aWAt4TWY", download=False)
