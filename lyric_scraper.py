import requests
from bs4 import BeautifulSoup
import re
import string
from time import sleep
import random
import pickle
import urllib
from urllib2 import urlopen
import os
from hashlib import sha1    
    
def get_songs(proxies, user_agents, artists):
    """takes a list of dictionaries for request"""
    base = 'http://www.azlyrics.com/'
    art_song_dict = {}
    for artist in artists:    
        url = base + artist[0] + '/' + artist + '.html'
        sleep(random.randint(0,10))
        response = requests.get(url, headers = {'User-Agent': random.choice(user_agents)}, proxies=random.choice(proxies))
        soup = BeautifulSoup(response.content, 'html')
        lang = []
        for song in soup.findAll(target='_blank'):
            lang.append(str(song.text))
        art_song_dict[artist] = lang
        # pickle.dump(art_song_dict, open(artist + '_songs.pickle', 'wb'))
    return art_song_dict

def sanitize_items(artist, song):
    return [re.sub('['+string.punctuation+']', '', artist).replace(' ','').lower(), re.sub('['+string.punctuation+']', '', song).replace(' ','').lower()]

def get_lyric_AZ(artist, song, user_agents):
    s_items = sanitize_items(artist, song)
    artist = s_items[0]
    song = s_items[1]
    url = 'http://www.azlyrics.com/lyrics/' + s_items[0] +'/' + s_items[1] + '.html'
    local_item = load_local(artist, song)
    if local_item != None:
        return local_item
    else:
        # sleep(random.randint(0,20))
        print('getting url', url)
        # response = requests.get(url);
        response = requests.get(url, headers = {'User-Agent': random.choice(user_agents)})
        # store_local(url, response.content)
        soup = BeautifulSoup(response.content, 'lxml')
        container = soup.findAll('div', {'class': 'col-xs-12 col-lg-8 text-center'})[0]
        lyric_list = container.text.strip().split('\n')
        lyrics = []
        idx = 8
        while lyric_list[idx].find('if  ( /Android|webOS|iPhone') == -1:
            tmp_lyric = lyric_list[idx].strip()
            idx += 1
            if (tmp_lyric == ''): continue
            lyrics.append(tmp_lyric)
        store_local(artist, song, lyrics)
        return lyrics
        # page_lyric = soup.findAll(style="margin-left:10px;margin-right:10px;")
        # page_lyric = soup.findAll(style="margin-left:10px;margin-right:10px;")
        # lyric = re.sub('[(<.!,;?>/\-)]', " ",  str(page_lyric)).split()
        # print(page_lyric)
        # lyric = [word for word in lyric if word != 'br']
        # print(lyric)
        return text


CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')

def url_to_filename(artist, song):
    #Make a URL into a file name, using SHA1 hashes. 
    if not os.path.isdir(CACHE_DIR+'/'+artist):
        os.makedirs(CACHE_DIR+'/'+artist)
    # use a sha1 hash to convert the url into a unique filename
    # hash_file = sha1(url).hexdigest() + '.html'
    hash_file = song+'.txt'
    return os.path.join(CACHE_DIR+'/'+artist, hash_file)


def store_local(artist, song, content):
     #Save a local copy of the file.

    # If the cache directory does not exist, make one.
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    # Save to disk.
    local_path = url_to_filename(artist, song)
    with open(local_path, 'wb') as f:
        for item in content:
            f.write(item+'\n')


def load_local(artist, song):
       # Read a local copy of a URL.
    local_path = url_to_filename(artist, song)
    if not os.path.exists(local_path):
        return None
    with open(local_path, 'rb') as f:
        lyrics_file = f.read().split('\n')
        lyrics = []
        for _l in lyrics_file:
            lyrics.append(_l)
        # return f.read()
        return lyrics



def main():
    # master_dict = {}
    # avg_dict = {}
    # with open('rush_songs.pickle', 'rb') as f:
        # art_info = pickle.load(f) 
    # for artist, songs in art_info.iteritems():
    # url = get_url_AZ()
    lyric = get_lyric_AZ('Sufjan Stevens', 'He Woke Me Up Again', user_agents)
    return lyric

    #     avg = []
    #     lyrics = []
    #     for song in songs:
    #         print artist, song
    #         url = get_url_AZ(artist,song)
    #         lyric = get_lyric_AZ(url, proxies, user_agents)
    #         print lyric
    #         avg.append(len(lyric))
    #         lyrics.append(lyric)
    #     avg_dict[artist] = avg
    #     master_dict[artist] = lyrics
    #     print artist, "-------------------------completed----------------------------------"
    #     pickle.dump(avg_dict, open(artist + '_count.pickle', 'wb'))
    #     pickle.dump(master_dict, open(artist + '_lyrics.pickle', 'wb'))
    # return 'Fully Completed!'

user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']
proxies = []
# proxies = [{"http": "http://107.170.13.140:3128"}, {"http": "http://198.23.67.90:3128"}]

#check_proxy(proxies)
foo = main()
