#!/usr/bin/env python3

import sys
import csv
import json
from langdetect import detect

# Export language pairs from EOAT dual-language markdown
# files to JSON or csv, with the first language specified as
# input and the second language string as the output.

def convert_to_markdown(text):
    escape_chars = {
        '*': '\\*', '_': '\\_', '~': '\\~', '>': '\\>', '<': '\\<',
        '#': '\\#', '+': '\\+', '-': '\\-', '=': '\\=', '[': '\\[',
        ']': '\\]', '{': '\\{', '}': '\\}', '(': '\\(', ')': '\\)',
        '!': '\\!',
    }
    return ''.join(escape_chars.get(char, char) for char in text)

def write_csv(data, output_file):
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        csv_writer = csv.writer(outfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['input_text', 'output_text'])  # Header names reflecting input/output concept
        for row in data:
            csv_writer.writerow([row['input_text'], row['output_text']])

def write_json(data, output_file, input_lang, output_lang):
    ordered_data = []
    for row in data:
        # Ensure the ordering for JSON is as per input_lang and output_lang
        ordered_row = {input_lang: row.get(input_lang, ''), output_lang: row.get(output_lang, '')}
        ordered_data.append(ordered_row)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(ordered_data, outfile, ensure_ascii=False, indent=4)

def main():
    if len(sys.argv) < 5:
        print("Usage: python", sys.argv[0], "[filename] [input lang code] [output lang code] [output format]")
        sys.exit(1)

    input_file, input_lang, output_lang, output_format = sys.argv[1:5]
    output_file = f"{input_file.rsplit('.', 1)[0]}_tuning_data.{'csv' if output_format == 'csv' else 'json'}"
    data = []

    try:
        with open(input_file, 'r', encoding='utf-8') as myfile:
            pending = {}
            for line in myfile:
                if line.isspace():
                    continue

                detected_lang = detect(line.strip())
                markdown_line = convert_to_markdown(line.strip())

                if detected_lang == input_lang:
                    pending['input_text'] = markdown_line
                elif detected_lang == output_lang:
                    pending['output_text'] = markdown_line

                if 'input_text' in pending and 'output_text' in pending:
                    # Append a copy of pending to avoid mutation issues
                    data.append(pending.copy())
                    pending.clear()

        if output_format == 'csv':
            write_csv(data, output_file)
        else:
            write_json(data, output_file, 'input_text', 'output_text')

        print(f"Successfully created tuning data file: {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

