# Natural Language Toolkit: Nasjonalbiblioteket Uttale CorpusReader
#
# Copyright (C) 2001-2023 NLTK Project
# Author: Ingerid Dale <ingerid.dale@nb.no>
# URL: <https://www.nltk.org/>
# For license information, see LICENSE.TXT

"""
NB Uttale is a Norwegian pronunciation dictionary,
with orthographic wordforms in the bokmål written standard,
and phonemic transcriptions for the Eastern Norwegian dialect in NoFAbet, an adjusted version of ARPAbet.
There are 819856 word-transcription pairs (WTP) in the lexicon.

The code here has been copied from the cmudict CorpusReader and adjusted to fit NB Uttale.

File format:
Each line consists of a lower case or title case word (e.g. proper names), and its transcription.
Multiword expressions are written with tilda (~) between the words.
Vowels are marked for stress (1=primary, 2=secondary, 0=no stress).

Example:
ordbok  OO2 R B OO3 K
over~bord       OA3 V AEH0 R ~ B OO1 R
Cuba    K UU1 B AH0

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
                StreamBackedCorpusView(fileid, read_pronlex_block, encoding=enc)
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


def read_pronlex_block(stream):
    entries = []
    while len(entries) < 100:  # Read 100 at a time.
        line = stream.readline()
        if line == "":
            return entries  # end of file.
        pieces = line.split()
        entries.append((pieces[0].lower(), pieces[1:]))
    return entries
