# CyberDrop Downloader


### Intro
Let's suppose you found out the Eva G (bby_gee) leak on [https://cyberdrop.me/a/aWAt4TWY](https://cyberdrop.me/a/aWAt4TWY). You wish you could download the entire gallery in a row. But there is not any download button. No problem, I fixed that for you.
![Eva G leaked pack blurred](assets/img/cyberdrop_bby_gee.png)

### Setup
First of all, clone this repository :

```bash
~$ git clone https://github.com/quatrecentquatre-404/cyberdrop-downloader
```

Second, oh wait... There is not a second part, because it does not require any extra module.

### Config
Open up the ``tests.py`` file and scroll all the way down. You will find this line :
```python
main(username="bby_gee", short_code="aWAt4TWY", download=False)
```

``username`` : the folder's name that will be created in the ``download`` directories, where all files will be downloaded, and where the ``meta.json`` file, that contains all URL found and downloaded, will be placed.

``short_code`` : the CyberDrop URL's ID.

``download`` : download files if ``True``, else, do nothing than write URLs on the ``meta.json`` file.

Now, you can figure out by yourself what to put in these quotes to download all the leaks you want.

### Run it !
Once you've updated all the config, you can run the script :
```bash
python3 tests.py
```
And there you go !

### Thanks !
I hope you enjoy my work. If you do, please, ⭐ this repository. If you have anything to report or to update, you can open an issue or a pull request, I'll give a look for sure.
