#!/usr/bin/env python3

from guess_language import guessLanguage

enguess = guessLanguage('hi')

if str(enguess) == 'en':
    print("PASS")
else:
    print("FAIL")
