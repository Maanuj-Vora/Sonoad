import saavn
import json
import download


songOrAlbumOrPlaylist = int(input("""

[0] Song
[1] Album
[2] Playlist

"""))

if songOrAlbumOrPlaylist == 0:
    song = input('Song: ')
    query = saavn.search_for_song(song, True)[0]
    download.downloadSong('song', query)

elif songOrAlbumOrPlaylist == 1:
    song = input('Album: ')
    id = saavn.get_album_id(song)
    query = saavn.get_album(id,True)
    download.downloadSongs('song', query)

elif songOrAlbumOrPlaylist == 2:
    song = input('Playlist: ')
    id = saavn.get_playlist_id(song)
    query = saavn.get_playlist(id,True)
    download.downloadSongs('song', query)