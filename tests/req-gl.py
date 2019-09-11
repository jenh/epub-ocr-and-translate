#!/usr/bin/env python

from guess_language import guessLanguage

enguess = guessLanguage('hi')

if str(enguess) == 'en':
    print("PASS")
else:
    print("FAIL")
