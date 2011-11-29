#!/usr/bin/python
import csv
import sys
import time
import re
import sets

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
        #words = splitter.split(string)
        words = string.split()
        for word in words:
            dm_word = metaphone.dm(word)
            l = len(word)
            if maxlen < l:
                maxlen = l

            if dm_word in res:
                res[dm_word].add(string)
            else:
                res[dm_word] = set(string)

            #if (dm_word[0] != dm_word[1]) & (len(dm_word[1]) > 0):
            #  print "'" + word + "' --> '" + dm_word[0] + " / " + dm_word[1]
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

    print 'Search took ' + str(time.clock() - c) + ' seconds'

    for art, score in scoredArtists:
        if score > 80:
            print str(score) + " ==> '" + art + "'"

    return None



def search_for_song_exact(artists, artistname, albumname, songname):
    c = time.clock()
    artistDict = dict()
    # score artists names:
    for artistName, albums in artists.iteritems():
        artistDict[artistName] = (artistname == artistName)
        #artistDict[artistName] = fuzz.token_set_ratio(artistname, artistName)
        #artistDict[artistName] = fuzz.token_sort_ratio(artistname, artistName)

    # sort by relevance:
    scoredArtists = sorted(artistDict.iteritems(), key=lambda (k,v): (v,k))

    print 'Search took ' + str(time.clock() - c) + ' seconds'

    for art, score in scoredArtists:
        if score == True:
            print str(score) + " ==> '" + art + "'"

    return None


def search_song_loop(songdb):
  while 1:
    artistname = raw_input("Enter artist name >  ")
    albumname = raw_input("Enter album name >  ")
    songname = raw_input("Enter song name >  ")

    result = search_for_song_exact(songdb, artistname, albumname, songname)

    if result != None:
      print "found '" + result[2] + "'"
      print "by '" + result[0] + "'"
      print "from album '" + result[1] + "'"
    else:
      print "not result found\n\n"

def search_words_loop(wordlist, songdb):
    splitter = re.compile(r'([ \t])')
    while 1:
        artistname = raw_input("Enter artist name >  ")
        c = time.clock()

        if (artistname in songdb):
            c = time.clock() - c
            print "Found '" + artistname + "'"
        else:
            #words = splitter.split(artistname)
            words = artistname.split()

            output = set()
            for word in words:
                if ((word[0] != ' ') | (word[0] != '\t')):
                    cc = time.clock()
                    word_dm = metaphone.dm(word)
                    for aword, source in wordlist.iteritems():
                        if word_dm == aword:
                            for elem in source:
                                output.add(elem)
                    print "word '" + word + "' took " + str(time.clock() - cc) + ' seconds'
            print '    step 1 took ' + str(time.clock() - c) + ' seconds'
            print '    ' + str(len(output)) + ' artists left'

            artistDict = dict()
            for out in output:
                ratio = fuzz.token_sort_ratio(artistname, out)
                #if ratio >= 0:
                artistDict[out] = ratio

            print '    step 2 took ' + str(time.clock() - c) + ' seconds'
            # sort by relevance:
            scoredArtists = sorted(artistDict.iteritems(), key=lambda (k,v): (v,k))

            #for name, score in scoredArtists:
            #  print str(score) + " --> '" + name + "'"

            c = time.clock() - c

            for art, score in scoredArtists[-5:]:
                print str(score) + " ==> '" + art + "'"
                #print str(ratio) + " --> '" + out + "'"

        print 'Search took ' + str(c) + ' seconds'

######################################## Index Class:
class Index:
    """A class that implements fast fuzzy lookup of text for artist, song and album lists"""

    def f(self):
        return 'hello world'





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

        # common words:
        common_words = { "the", "for", "a", "of", 'and' }
        for w in common_words:
            if w in artists_words:
                del artists_words[w]

        #search_song_loop(songdb)
        search_words_loop(artists_words, songdb)
    else:
      print "Usage: " + sys.argv[0] + " csv_filename"


if __name__ == '__main__':
  main()

