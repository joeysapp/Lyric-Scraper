import requests, re, string, os
from bs4 import BeautifulSoup
from time import sleep

# Returns [artist, song] in url escaped format
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
        print('getting url', url)
        response = requests.get(url, headers = {'User-Agent': random.choice(user_agents)})
        soup = BeautifulSoup(response.content, 'lxml')
        container = soup.findAll('div', {'class': 'col-xs-12 col-lg-8 text-center'})[0]
        lyric_list = container.text.strip().split('\n')
        lyrics = []
        idx = 8 # Arbitrarily found this, 7 is the title of song
        while lyric_list[idx].find('if  ( /Android|webOS|iPhone') == -1:
            tmp_lyric = lyric_list[idx].strip()
            idx += 1
            if (tmp_lyric == ''): continue
            lyrics.append(tmp_lyric)
        store_local(artist, song, lyrics)
        return lyrics

CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')

def url_to_filename(artist, song):
    if not os.path.isdir(CACHE_DIR+'/'+artist):
        os.makedirs(CACHE_DIR+'/'+artist)

    hash_file = song+'.txt'
    return os.path.join(CACHE_DIR+'/'+artist, hash_file)


def store_local(artist, song, content):
    # Save a local copy of the file.

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
        return lyrics

def main():
    lyric = get_lyric_AZ('Sufjan Stevens', 'He Woke Me Up Again', user_agents)
    return lyric

user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']

foo = main()
