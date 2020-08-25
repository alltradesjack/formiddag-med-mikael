from bs4 import BeautifulSoup
import requests


def get_headers():
    return {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", 
            "Accept-Encoding":"gzip, deflate",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "DNT":"1","Connection":"close",
            "Upgrade-Insecure-Requests":"1"}


def get_newest_episode():

    headers = get_headers()
    r = requests.get('https://www.dr.dk/radio/p6beat/formiddag-med-simpson/', headers=headers)
    content = r.content
    soup = BeautifulSoup(content, features="html.parser")

    for d in soup.findAll('div', attrs={'class':'series-featured__latest-episode'}):
        newest_episode = 'https://www.dr.dk' + d.find('a', href=True)['href']

    return newest_episode


def get_episode_playlist(episode_link):
    
    headers = get_headers()
    r = requests.get(episode_link, headers=headers)
    content = r.content
    soup = BeautifulSoup(content, features="html.parser")

    artists = []
    tracks = []
    for d in soup.findAll('li', attrs={'class':'index-point index-point--has-artist'}):
        artists.append(d.find('span', attrs={'class':'playlist-item-artist-line'}).text)
        tracks.append(d.find('h3', attrs={'class':'index-point__title'}).text)
    
    return (artists, tracks)
