import argparse
import json
import logging
import os
import re
import sys

from prettytable import PrettyTable
from collections import Counter
from functools import partial

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

BASE_DATA_DIR = os.path.realpath(os.path.join(os.getcwd(), "data"))

NOISE_WORDS = ['and', 'we', 'I', 'the', 'an', "Let", "to", "all", "It's", "in", "a",
               "me", "because", "you", "for", "my", "this", "can", "be", "of", "by",
               "there", "In", "that's", "us", "too", "what's", "more", "on", "who've",
               "but", "me,", ",", "That's", "As", "am", "not", "that", "was", "or", "be",
               "their", "than", "our", "by", "as", "and", "And", "then", "But", "is", "have",
               "-", "with", "are", "it", "who", "from", "has", "what", "about", "been", "they",
               "The", "at", "We", "just", "know", "so", "those", "these", "he", "when", "will",
               "if", "It", "?", "where", "his", "she", "your", "must", "also", "had", "would",
               "don't", "do", "how", "were", "every", "could", "after", "them", "her", "against",
               "here", ]


class HashTags(object):
    def __init__(self, first=5, base_dir=BASE_DATA_DIR, full_document_path=False):
        self._new_filtered_words = []
        self.first = first
        self.base_dir = base_dir
        self.full_document_path = full_document_path

    def _get_absolute_file_path(self):
        # to get absolute file path
        for dir_path, _, filename in os.walk(self.base_dir):
            for f in filename:
                yield os.path.abspath(os.path.join(dir_path, f))

    def _accepted_document(self, path):
        # to check if this file is accepted to search in
        return path.endswith('.txt')

    def _get_file_contents(self, search_sentences=False):

        for path in self._get_absolute_file_path():
            if self._accepted_document(path):
                with open(path, 'r') as p:
                    for chunk in iter(partial(p.read, 1048), ''):
                        if not search_sentences:
                            yield chunk.split()
                        else:
                            yield path, chunk

    def filter_words(self):
        self._new_filtered_words = ''.join([' '.join(w for w in word
                                                     if w not in NOISE_WORDS)
                                            for word in self._get_file_contents()
                                            ]).split()

    @property
    def _non_filter_words(self):
        # Not Filtering any Noise words
        return [w for word in self._get_file_contents() for w in word]

    def _get_word_occurrences(self):
        # Get word occurrences filter or non filter data
        if self._new_filtered_words:
            return Counter(self._new_filtered_words)
        return Counter(self._non_filter_words)

    def _get_most_common(self):
        # Get Most common words using the Counter
        if isinstance(self._get_word_occurrences(), Counter):
            return self._get_word_occurrences().most_common(self.first)

    def _get_sentences(self):
        # Get Sentences from most common tags
        regex = "([^.]*?{0}[^.]*[\.|\\n])"
        most_common = self._get_most_common()
        tags = (k for key in most_common for k in key[0::2])
        for tag in tags:
            for path, texts in self._get_file_contents(search_sentences=True):
                for sentences in re.findall(regex.format(tag), texts):
                    yield tag, path, sentences.strip()

    def prepare_data(self):
        self.data = {}
        logger.info("Preparing Sentences.....")
        for tag, path, sentence in self._get_sentences():
            if not self.full_document_path:
                path = path.rsplit("/")[-1]
            if tag not in self.data:
                self.data[tag] = {}
                self.data[tag]['paths'] = list()
                self.data[tag]['sentences'] = list()
                self.data[tag]['paths'].append(path)
                self.data[tag]['sentences'].append(sentence)
            elif tag in self.data and path not in self.data[tag]['paths']:
                self.data[tag]['paths'].append(path)
                self.data[tag]['sentences'].append(sentence)
            elif tag in self.data and path in self.data[tag]['paths']:
                self.data[tag]['sentences'].append(sentence)

    def output_json(self, to_file=None):
        '''
        Prepared data to json output
        :return: json
        '''
        if hasattr(self, 'data'):
            output = json.dumps(self.data, indent=4)
            if to_file is not None:
                logger.info("Generate file %s", to_file)
                with(open(to_file, 'w')) as out:
                    out.write(output)

    def display(self, in_file=None):
        '''
        Pretty Print Table
        :param in_file: Input the file for displaying the output from json
        :return: table [PrettyTable]
        '''
        if in_file is not None:
            logger.info("Reading file %s", in_file)
            with(open(in_file, 'r')) as input:
                data = json.load(input)

            table = PrettyTable(["Word(#)", "Documents", "Sentences containing the word"])
            table.align["Sentences containing the word"] = "l"  
            for key in data:
                table.add_row([key, ", \n".join(data[key]['paths']),
                                self._insert_new_lines("\n\n".join(data[key]['sentences']), 100)])

            return table

    def _insert_new_lines(self, text, lineLength):
        # Insert new lines for pretty print the table

        if len(text) <= lineLength:
            return text
        else:
            return "".join([text[:lineLength], '\n', self._insert_new_lines(text[lineLength:], lineLength)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--first", help="Get the first few common words, Default is 5", type=int)
    parser.add_argument("-f", "--filter", help="Filter out all punctuations, articles and any other unnecessary words",
                        action='store_true', default=False)
    parser.add_argument("-v", "--verbose", help="Increase logging level to Debug",
                        action='store_true')
    parser.add_argument("-o", "--output", help="Output JSON",
                        action='store', required=True)
    parser.add_argument("-d", "--data-dir", help="Directory to which the files to be searched,"
                                            " Default is project's data directory",
                        action='store', dest="directory")
    parser.add_argument("-i", "--display", help="View the output in tabular format",
                        action='store_true')
    parser.add_argument("-fdp", "--full-document-path", help="Get the full document path",
                        action='store_true', dest="full_document_path")
    parser.add_argument("-s", "--set-recursion-limit",
                        help="Increase the recursion limit for getting output, current recursion limit is {0}".format(
                        sys.getrecursionlimit()), type=int, dest = "set_recursion_limit")


    args = parser.parse_args()

    if args.set_recursion_limit:
        sys.setrecursionlimit(args.set_recursion_limit)

    if args.output:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    ht = HashTags()
    if args.directory:
        if os.path.isdir(args.directory):
            ht.base_dir = args.directory

    if args.first:
        ht.first = args.first
    if args.filter:
        ht.filter_words()

    if args.full_document_path:
        ht.full_document_path = args.full_document_path

    ht.prepare_data()

    if args.output:
        ht.output_json(to_file=args.output)

    if args.display and args.output:
        print(ht.display(args.output))
    elif args.display and not args.output:
        logger.info("Use -o filename.txt to display")

