
# Anagram Bot

_A Discord bot that randomly finds anagrams in text channel messages_

## Description

This bot watches messages in text channels, and randomly picks out some
messages to search for anagrams. It then scans through short phrases from
those messages, searching for combinations of common words that form anagrams
of the chosen phrases, and sends a message in chat if one is found.

## Installation

1. Create a text file called `token.txt` containing the secure token for your
   bot account. The bot will read the token from this file rather than keeping
   the token in the source code.

2. Install the required Python library `discord`, for example by
    ```
    $ pip3 install discord --user
    ```

3. You can now start the bot with
    ```
    $ python3 bot.py
    ```

