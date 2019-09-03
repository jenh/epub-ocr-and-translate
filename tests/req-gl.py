#!/usr/bin/env python2.7

from guess_language import guessLanguage

enguess = guessLanguage('hi')

if str(enguess) == 'en':
    print "PASS"
else:
    print "FAIL"
