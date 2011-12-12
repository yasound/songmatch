######################################## Index Class:

import re
import sets
import metaphone
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class StringIndex():
    """A class that implements fast fuzzy lookup of text for artist, song and album lists"""

    def __init__(self):
        self.maxlen = 0
        self.strings = set()
        self.index = dict()
        self.splitter = re.compile(r'([ \t])')

    def add(self, string):
        words = string.split()
        for word in words:
            dm_word = metaphone.dm(word)
            l = len(word)
            if self.maxlen < l:
                self.maxlen = l

            if dm_word in self.index:
                self.index[dm_word].add(string)
            else:
                self.index[dm_word] = set(string)

    def __len__(self):
        return len(self.index)

    def get_best_items(self, key):
        if (key in self.strings):
            return key
        else:
            #words = splitter.split(artistname)
            words = key.split()

            output = set()
            for word in words:
                if ((word[0] != ' ') | (word[0] != '\t')):
                    word_dm = metaphone.dm(word)
                    for aword, source in self.index.iteritems():
                        if word_dm == aword:
                            for elem in source:
                                output.add(elem)

            stringDict = dict()
            for out in output:
                ratio = fuzz.token_sort_ratio(key, out)
                #if ratio >= 0:
                stringDict[out] = ratio

            # sort by relevance:
            scoredStrings = sorted(stringDict.iteritems(), key = lambda (k,v): (v,k))

            #for name, score in scoredArtists:
            #  print str(score) + " --> '" + name + "'"

            #for art, score in scoredStrings[-5:]:
                #print str(score) + " ==> '" + art + "'"
                #print str(ratio) + " --> '" + out + "'"
            return scoredStrings


    def __getitem__(self, key):
        items = self.get_best_items(key)
        for artist, score in items[-1:]:
            return artist

    def set_common_words(self, words):
        for w in words:
            if w in self.index:
                del self.index[w]

