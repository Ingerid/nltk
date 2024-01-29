"""
NB Uttale is a Norwegian pronunciation dictionary,
with orthographic wordforms in the bokmål written standard,
and phonemic transcriptions for the Eastern Norwegian dialect in SAMPA.
"""

from nltk.corpus.reader.api import *
from nltk.corpus.reader.util import *
from nltk.util import Index


class NBUttaleCorpusReader(CorpusReader):
    def entries(self):
        """
        :return: the nb_uttale lexicon as a list of entries
            containing (word, transcriptions) tuples.
        """
        return concat(
            [
                StreamBackedCorpusView(fileid, read_cmudict_block, encoding=enc)
                for fileid, enc in self.abspaths(None, True)
            ]
        )

    def words(self):
        """
        :return: a list of all words defined in the nb_uttale lexicon.
        """
        return [word.lower() for (word, _) in self.entries()]

    def dict(self):
        """
        :return: the nb_uttale lexicon as a dictionary, whose keys are
            lowercase words and whose values are lists of pronunciations.
        """
        return dict(Index(self.entries()))


def read_cmudict_block(stream):
    entries = []
    while len(entries) < 100:  # Read 100 at a time.
        line = stream.readline()
        if line == "":
            return entries  # end of file.
        pieces = line.split()
        entries.append((pieces[0].lower(), pieces[1:]))
    return entries
