"""
Auto Anime Folder Renamer
Patrick Serrano
2-12-2021

This will rename folder in the current directory. It does this by:
1. Looks a folder in the current directory and cleans it up
2. Searches MAL for the scrapes for corresponding anime entry (Google searching was supported but it can lead to getting
rate limited (HTTPError 429) and prevents functionality)
3. Adds a '~' to the end of file to determine that that file has been formatted
4. Files that cannot be properly named are prepended by an '@'
5. If wrong MAL link is found then enter 'n' and enter the correct MAL link

⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⢀⣀⣀⡀⠄⠄⠄⡠⢲⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠄⠄
⠄⠄⠄⠔⣈⣀⠄⢔⡒⠳⡴⠊⠄⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣧⠄⠄
⠄⢜⡴⢑⠖⠊⢐⣤⠞⣩⡇⠄⠄⠄⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠄⠝⠛⠋⠐
⢸⠏⣷⠈⠄⣱⠃⠄⢠⠃⠐⡀⠄⠄⠄⠄⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠸⠄⠄⠄⠄
⠈⣅⠞⢁⣿⢸⠘⡄⡆⠄⠄⠈⠢⡀⠄⠄⠄⠄⠄⠄⠉⠙⠛⠛⠛⠉⠉⡀⠄⠡⢀⠄⣀
⠄⠙⡎⣹⢸⠄⠆⢘⠁⠄⠄⠄⢸⠈⠢⢄⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠃⠄⠄⠄⠄⠄
⠄⠄⠑⢿⠈⢆⠘⢼⠄⠄⠄⠄⠸⢐⢾⠄⡘⡏⠲⠆⠠⣤⢤⢤⡤⠄⣖⡇⠄⠄⠄⠄⠄
⣴⣶⣿⣿⣣⣈⣢⣸⠄⠄⠄⠄⡾⣷⣾⣮⣤⡏⠁⠘⠊⢠⣷⣾⡛⡟⠈⠄⠄⠄⠄⠄⠄
⣿⣿⣿⣿⣿⠉⠒⢽⠄⠄⠄⠄⡇⣿⣟⣿⡇⠄⠄⠄⠄⢸⣻⡿⡇⡇⠄⠄⠄⠄⠄⠄⠄
⠻⣿⣿⣿⣿⣄⠰⢼⠄⠄⠄⡄⠁⢻⣍⣯⠃⠄⠄⠄⠄⠈⢿⣻⠃⠈⡆⡄⠄⠄⠄⠄⠄
⠄⠙⠿⠿⠛⣿⣶⣤⡇⠄⠄⢣⠄⠄⠈⠄⢠⠂⠄⠁⠄⡀⠄⠄⣀⠔⢁⠃⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⣿⣿⣿⣿⣾⠢⣖⣶⣦⣤⣤⣬⣤⣤⣤⣴⣶⣶⡏⠠⢃⠌⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠿⠿⠟⠛⡹⠉⠛⠛⠿⠿⣿⣿⣿⣿⣿⡿⠂⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
⠠⠤⠤⠄⠄⣀⠄⠄⠄⠑⠠⣤⣀⣀⣀⡘⣿⠿⠙⠻⡍⢀⡈⠂⠄⠄⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⠑⠠⣠⣴⣾⣿⣿⣿⣿⣿⣿⣇⠉⠄⠻⣿⣷⣄⡀⠄⠄⠄⠄⠄⠄⠄⠄
"""
import os
import re
from datetime import time
import requests
from bs4 import BeautifulSoup as bs
from googlesearch import search
from urllib.error import HTTPError


def clean(FileName):
    FileName = re.sub("\[.*?\]", "", FileName)
    return FileName


def search_google(anime_name):
    # SearchResults = search("MyAnimeList " + anime_name + " -nyaa.si", num_results=2)
    SearchResults = search("site:myanimelist.net " + anime_name + " -nyaa.si", num_results=2)
    print(SearchResults)
    return SearchResults[0]


def search_mal(anime_name):
    searcher = 'https://myanimelist.net/anime.php?q='
    searcher = searcher + anime_name
    mal = requests.get(searcher)
    soup = bs(mal.content, features="html.parser")
    a = soup.find_all("a")
    target = str(a[90])
    target = re.findall(r'(https?://[^\s]+)', target)
    target = str(target)
    target = target[2:-8]
    return target


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def find_Title(url):
    mal = requests.get(url)
    soup = bs(mal.content, features="html.parser")
    h1 = soup.find_all("h1")[0]
    japName = clean_html(str(h1))
    p = soup.find_all("p")[0]
    EnName = clean_html(str(p))
    illegal = ['*', '.', '"', "\\", '/', '[', ']', ':', ';', '|', ',', '?']
    for char in illegal:
        japName = japName.replace(char, '')
        EnName = EnName.replace(char, '')

    if (len(EnName) > 100):
        return japName, "NO ALT NAME"
    return japName, EnName


def name_format(jName, eName):
    if (eName == "NO ALT NAME"):
        return jName+"~"
    return f'{jName} ({eName})~'


def main(file):
    cleaned = clean(file)
    print(f"\nThe current file is {file}")
    Result = search_mal(cleaned)
    userInp = ''
    correct = ''
    while userInp not in ['y', 'n']:
        userInp = input(f'Is this the correct link? (y,n)\n{Result}\n')

    if userInp == 'n':
        print("Do this manually. MAL returned unexpected result.")
        print('Enter correct MAL link.')
        correct = input()
        print()
        Result = correct

    t = find_Title(Result)
    name = name_format(t[0], t[1])

    userInp = ''
    while userInp not in ['y', 'n']:
        userInp = input(f'Is this the correct name? (y,n)\n{name}\n')

    if userInp == 'n':
        print("Do this manually. Name will not be Changed.")
        return

    return name


# Change the current directory here
directory = r"Z:\Downloads\completed"

os.chdir(directory)
i = 0
x = []
for f in os.listdir():
    x.append(f)

for file in x:
    if os.path.isdir(file):
        try:
            currFile = file
            if currFile[-1:] == '~':
                print(f'File was not changed: {currFile}')
                print("~" * 50)
                continue
            newName = main(file)
            os.rename(file, newName)
            print(f'File name change:\n{currFile}\n{newName}')
            print("~"*50)

        except Exception as e:
            print("You made a fucky wucky.")
            print(e)
            print('Adding a marker')
            os.rename(file, '@' + file)
        except HTTPError as h:
            time.sleep(5)
            print("Dang we fucked up fam.")

    else:
        print(f'"\n{file}" is not a folder.')
