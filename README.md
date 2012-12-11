manga-dl
========

Manga downloader

Current downloads only from one site, because the page attributes are hard code. 
Need to change from that to rule based scraping for each manga site or at least the major ones

At the moment, it works only to download the jpgs for the mangas you select using the command line utility.

Requirements:
Python 2.7
SQLAlchemy 0.8
Sqlite3 - Not necessary

usage:
python main.py "name of manga" "url for the rss feed (xml) for the manga" "path to the download folder"

As a python newbie, I would really appreciate any kind of improvements in the code. Especially, related to 
unit testing and code architecture. 

Please send the patches to arshadansari27@gmail.com with subject line [manga-dl]





