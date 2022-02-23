#!/bin/env python3

##
## AnagramBot
## (C) 2022 Christopher Ptak 
##
## A Discord bot that randomly finds anagrams in text channel messages
##

import random
import re

from collections import defaultdict
from copy import deepcopy

import discord

class LetterCount:

    def __init__(self, word):
        self.total = len(word)
        self.counts = [0] * (ord('Z') - ord('A') + 1)
        for letter in word.upper():
            i = ord(letter) - ord('A')
            self.counts[i] += 1

    def contains(self, other):
        for i in range(len(other.counts)):
            if other.counts[i] > self.counts[i]:
                return False
        return True

    def add(self, other):
        self.total += other.total
        for i in range(len(other.counts)):
            self.counts[i] += other.counts[i]

    def remove(self, other):
        self.total -= other.total
        for i in range(len(other.counts)):
            self.counts[i] -= other.counts[i]
            assert self.counts[i] >= 0

    def empty(self):
        return self.total == 0


class AnagramFinder:

    def __init__(self):
        self.words = {}
        with open('words.txt') as f:
            for line in f.readlines():
                word = line.strip().upper()
                self.words[word] = LetterCount(word)

    def find_with_letters(self, letters):
        mutable_letters = deepcopy(letters)
        for result in self._find_with_letters(mutable_letters):
            yield result

    def _find_with_letters(self, letters):
        if letters.empty():
            yield []
        for candidate in self.words:
            candidate_letters = self.words[candidate]
            if letters.contains(candidate_letters):
                letters.remove(candidate_letters)
                for result in self._find_with_letters(letters):
                    yield [candidate] + result
                letters.add(candidate_letters)


class AnagramClient(discord.Client):

    CONSECUTIVE_WORDS = 3
    MAX_PHRASE_LEN = 25

    def __init__(self):
        super().__init__()
        self.finder = AnagramFinder()

    def choose_phrases(self, text, n=None):
        phrases = []
        for section in re.split(r'[^\sA-Z]+', text.upper()):
            phrase = section.strip().split()
            if len(phrase) > AnagramClient.CONSECUTIVE_WORDS - 1:
                phrases.append(phrase)
        for phrase in phrases:
            for i in range(len(phrase) - (AnagramClient.CONSECUTIVE_WORDS - 1)):
                words = phrase[i:i+AnagramClient.CONSECUTIVE_WORDS]
                if sum(map(len, words)) <= AnagramClient.MAX_PHRASE_LEN:
                    yield words

    def find_anagram(self, phrase):
        letters = LetterCount(''.join(phrase))
        try:
            phrase_text = ' '.join(phrase)
            print('Looking for anagram of {}... '.format(phrase_text), end='', flush=True)
            anagram = next(self.finder.find_with_letters(letters))
            print('Found {}'.format(' '.join(anagram)))
            return anagram
        except StopIteration:
            print('None found')

    async def on_ready(self):
        print('Started AnagramClient')

    async def on_message(self, message):
        # Ignore our own messages
        if message.author == self.user:
            return
        # Only search one in every 10 messages
        if random.randint(0, 9) != 0:
            return
        for phrase in self.choose_phrases(message.content):
            anagram = self.find_anagram(phrase)
            if anagram is None:
                continue
            # Reply with the anagram
            phrase_text = ' '.join(phrase)
            anagram_text = ' '.join(anagram)
            reply = phrase_text + ' is an anagram for ' + anagram_text
            await message.channel.send(reply)
            break

token = open('token.txt', 'r').read()

client = AnagramClient()
client.run(token)

