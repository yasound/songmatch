import csv
import sys
import time
import re

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import metaphone

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

def build_wordlist(list_of_strings):
  res = dict()
  maxlen = 0
  splitter = re.compile(r'([ \t])')
  for string in list_of_strings:
    words = splitter.split(string)
    for word in words:
      dm_word = metaphone.dm(word)
      l = len(word)
      if maxlen < l:
        maxlen = l

      if dm_word in res:
        res[dm_word].add(string)
      else:
        res[dm_word] = set(string)
  print "Maximum word length found: " + str(maxlen)
  return res


def search_for_song(artists, artistname, albumname, songname):
  c = time.clock()
  artistDict = dict()
  # score artists names:
  for artistName, albums in artists.iteritems():
    artistDict[artistName] = fuzz.ratio(artistname, artistName)
    #artistDict[artistName] = fuzz.token_set_ratio(artistname, artistName)
    #artistDict[artistName] = fuzz.token_sort_ratio(artistname, artistName)

  # sort by relevance:
  scoredArtists = sorted(artistDict.iteritems(), key=lambda (k,v): (v,k))

  print 'Search took ' + str(c) + ' seconds'

  for art, score in scoredArtists:
    if score > 80:
      print str(score) + " ==> '" + art + "'"

  return None

def search_song_loop(songdb):
  while 1:
    artistname = raw_input("Enter artist name >  ")
    albumname = raw_input("Enter album name >  ")
    songname = raw_input("Enter song name >  ")

    result = search_for_song(songdb, artistname, albumname, songname)

    if result != None:
      print "found '" + result[2] + "'"
      print "by '" + result[0] + "'"
      print "from album '" + result[1] + "'"
    else:
      print "not result found\n\n"

def search_words_loop(words):
  while 1:
    artistname = raw_input("Enter artist name >  ")

    output = set()
    word_dm = metaphone.dm(artistname)
    for word, source in words.iteritems():
      if word_dm == word:
        #output.add(source)
        print source
        print str(len(source))

    for out in output:
      print "found '" + out + "'"

################### Main:
def main():
  if (len(sys.argv) > 1):
    print 'Loading csv'
    c = time.clock()
    songdb = read_csv(sys.argv[1])
    c = time.clock() - c
    print 'in ' + str(c) + ' seconds'

    print "building word list..."
    c = time.clock()
    artists_words = build_wordlist(songdb)
    c = time.clock() - c
    print 'in ' + str(c) + ' seconds'
    print str(len(artists_words)) + " words found"

    #search_song_loop(songdb)
    search_words_loop(artists_words)
  else:
    print "Usage: " + sys.argv[0] + " csv_filename"


if __name__ == '__main__':
  main()

