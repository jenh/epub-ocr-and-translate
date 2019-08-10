import sys
import textwrap
import time
from google.cloud import translate

input_file = sys.argv[1]
lang = sys.argv[2]
doc = []
output_file = input_file + "-en.md"

translate_client = translate.Client()

output_file = open(output_file,'w')

max_length = 4000
with open(input_file) as input:
    for line in input:
        lines = textwrap.wrap(line, max_length)
        for line in lines:
            doc.append(line)

for x in doc:
    output_file.write("\n\n" + x + "\n\n")
    time.sleep(2)
    translation = translate_client.translate(
        x,
    target_language=lang)
    output_file.write(translation['translatedText'].encode("utf-8") + "\n\n")
