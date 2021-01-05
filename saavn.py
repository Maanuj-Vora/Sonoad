import requests
import json
from traceback import print_exc
import base64
from pyDes import *
import saavn_url

def format_song(data,lyrics):
    try:
        url = data['media_preview_url']
        url = url.replace("preview", "aac")
        if data['320kbps']=="true":
            url = url.replace("_96_p.mp4", "_320.mp4")
        else:
            url = url.replace("_96_p.mp4", "_160.mp4")
        data['media_url'] = url
    except KeyError or TypeError:
        data['media_url'] = decrypt_url(data['encrypted_media_url'])
        if data['320kbps']!="true":
            data['media_url'] = data['media_url'].replace("_320.mp4","_160.mp4")

    data['song'] = format(data['song'])
    data['music'] = format(data['music'])
    data['singers'] = format(data['singers'])
    data['starring'] = format(data['starring'])
    data['album'] = format(data['album'])
    data["primary_artists"] = format(data["primary_artists"])
    data['image'] = data['image'].replace("150x150","500x500")

    if lyrics:
        if data['has_lyrics']=='true':
            data['lyrics'] = get_lyrics(data['id'])
        else:
            data['lyrics'] = None

    try:
        data['copyright_text'] = data['copyright_text'].replace("&copy;","©")
    except KeyError:
        pass
    return data

def format_album(data,lyrics):
    data['image'] = data['image'].replace("150x150","500x500")
    data['name'] = format(data['name'])
    data['primary_artists'] = format(data['primary_artists'])
    data['title'] = format(data['title'])
    for song in data['songs']:
        song = format_song(song,lyrics)
    return data

def format_playlist(data,lyrics):
    data['firstname'] = format(data['firstname'])
    data['listname'] = format(data['listname'])
    for song in data['songs']:
        song = format_song(song,lyrics)
    return data

def format(string):
    return string.encode().decode('unicode-escape').replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'")

def decrypt_url(url):
    des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0",pad=None, padmode=PAD_PKCS5)
    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
    dec_url = dec_url.replace("_96.mp4", "_320.mp4")
    return dec_url

def search_for_song(query,lyrics):
    if query.startswith('http') and 'saavn.com' in query:
        id = get_song_id(query)
        return get_song(id, lyrics)

    search_base_url = saavn_url.search_base_url+query
    response = requests.get(search_base_url).text.encode().decode('unicode-escape')
    response = json.loads(response)
    song_response = response['songs']['data']
    songs = []
    for song in song_response:
        id = song['id']
        song_data = get_song(id, lyrics)
        if song_data:
            songs.append(song_data)
    return songs

def get_song(id,lyrics):
    try:
        song_details_base_url = saavn_url.song_details_base_url+id
        song_response = requests.get(song_details_base_url).text.encode().decode('unicode-escape')
        song_response = json.loads(song_response)
        song_data =format_song(song_response[id],lyrics)
        if song_data:
            return song_data
    except:
        return None

def get_song_id(url):
    res = requests.get(url, data=[('bitrate', '320')])
    try:
        return res.text.split('"song":{"type":"')[1].split('","image":')[0].split('"id":"')[-1]
    except IndexError:
        return(res.text.split('"pid":"'))[1].split('","')[0]

def get_album(album_id,lyrics):
    songs_json = []
    try:
        response = requests.get(saavn_url.album_details_base_url+album_id)
        if response.status_code == 200:
            songs_json = response.text.encode().decode('unicode-escape')
            songs_json = json.loads(songs_json)
            return format_album(songs_json,lyrics)
    except Exception as e:
        print(e)
        return None

def get_album_id(input_url):
    res = requests.get(input_url)
    try:
        return res.text.split('"album_id":"')[1].split('"')[0]
    except IndexError:
        return res.text.split('"page_id","')[1].split('","')[0]

def get_playlist(listId,lyrics):
    try:
        response = requests.get(saavn_url.playlist_details_base_url+listId)
        if response.status_code == 200:
            songs_json = response.text.encode().decode('unicode-escape')
            songs_json = json.loads(songs_json)
            return format_playlist(songs_json,lyrics)
        return None
    except Exception:
        print_exc()
        return None

def get_playlist_id(input_url):
    res = requests.get(input_url).text
    try:
        return res.split('"type":"playlist","id":"')[1].split('"')[0]
    except IndexError:
        return res.split('"page_id","')[1].split('","')[0]

def get_lyrics(id):
    url = saavn_url.lyrics_base_url+id
    lyrics_json = requests.get(url).text
    lyrics_text = json.loads(lyrics_json)
    return lyrics_text['lyrics']