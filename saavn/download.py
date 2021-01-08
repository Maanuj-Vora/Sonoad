import requests
import json
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC, APIC
from pydub import AudioSegment


def content(name, data):
    r=requests.get(data.get('media_url'))
    f=open(name,'wb')
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: 
            f.write(chunk)
    f.close()

    fileName = data.get('song').replace(' ', '_') + data.get('id') + ".mp3"

    mp4_version = AudioSegment.from_file(name, "mp4")
    mp4_version.export(fileName, format="mp3")

    try: 
        tags = ID3(fileName)
    except ID3NoHeaderError:
        tags = ID3()

    tags["TIT2"] = TIT2(encoding=3, text=data.get('song'))
    tags["TALB"] = TALB(encoding=3, text=data.get('album'))
    tags["TPE1"] = TPE1(encoding=3, text=data.get('singers'))
    tags["TCOM"] = TCOM(encoding=3, text=data.get('music'))

    tags.save(fileName)

def downloadSong(name, data):
    name=name+".mp4"
    content(name, data)

def downloadSongs(name, data):
    name=name+".mp4"
    for song in data.get('songs'):
        content(name, song)