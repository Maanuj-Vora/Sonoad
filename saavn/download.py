import requests
import json
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC, APIC
from pydub import AudioSegment
from moviepy.editor import *
import taglib

def content(name, data):
    r=requests.get(data.get('media_url'))
    f=open(name,'wb')
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: 
            f.write(chunk)
    f.close()

    fileName = "songs/" + data.get('song').replace(' ', '_') + data.get('id') + ".mp3"

    mp4 = r"song.mp4"

    audio = AudioFileClip(mp4)
    audio.write_audiofile(fileName)
    audio.close()

    song = taglib.File(fileName)
    song.tags['TITLE'] = [data.get('song')]
    song.tags["ALBUM"] = [data.get('album')]
    song.save()

def downloadSong(name, data):
    name=name+".mp4"
    content(name, data)

def downloadSongs(name, data):
    name=name+".mp4"
    for song in data.get('songs'):
        content(name, song)