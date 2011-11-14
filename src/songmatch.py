import csv
import sys
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def print_songs(songs):
  for songName in songs:
    print '\t\t' + songName

def print_albums(albums, func = print_songs):
  for albumName, songs in albums.iteritems():
    print '\t' + albumName
    func(songs)

def print_albums_titles(albums):
  for albumName, songs in albums.iteritems():
    print '\t' + albumName

def print_artists(artists, func = print_albums_titles):
  for artistName, albums in artists.iteritems():
    print artistName
    func(albums)


def read_csv(filename):
  with open(filename, 'rb') as f:
    reader = csv.reader(f)
    try:
      artists = dict()
      song_count = 0
      album_count = 0
      for row in reader:
        artist = row[5]
        album = row[3]
        song = row[1]

        # Add or find artist:
        if artist not in artists:
          d = dict()
          artists[artist] = d
        else:
          d = artists[artist]

        # Add the album to the artist:
        if album not in d:
          dd = list()
          d[album] = dd
          album_count += 1
        else:
          dd = d[album]

        # Add song to the album:
        dd.append(song)
        song_count += 1

      print "found " + str(song_count) + " songs by " + str(len(artists)) + " artists in " + str(album_count) + ' albums'
      return artists
    except csv.Error, e:
      sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
  return none


################### Main:
if (len(sys.argv) > 1):
  print 'Load csv\n'
  c = time.clock()
  a = read_csv(sys.argv[1])
  c = time.clock() - c
  print 'Import took ' + str(c) + ' seconds'
  #print_artists(a);
else:
  print "Usage: " + sys.argv[0] + " csv_filename"

print 'DONE\n'

