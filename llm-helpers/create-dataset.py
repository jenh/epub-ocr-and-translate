#!/usr/bin/env python3

import argparse
from langdetect import detect, LangDetectException
import csv
import json

# Export language pairs from EOAT dual-language markdown
# files to JSON or csv, with the first language specified as
# input and the second language string as the output, with
# an optional prompt preamble.

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
        csv_writer.writerow(['input_text', 'output_text'])
        for row in data:
            csv_writer.writerow([row['input_text'], row['output_text']])

def write_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Converts language pairs to CSV or JSON for model tuning.')
    parser.add_argument('input_file', help='Source file that contains language pairs from EOAT')
    parser.add_argument('lang1', help='ISO 639 language code for the prompt')
    parser.add_argument('lang2', help='ISO 639 language code for the response')
    parser.add_argument('-o', '--output', default='json', choices=['csv', 'json'], help='Output file format. Defaults to JSON')
    parser.add_argument('-p', '--preamble', default="", help='Optional preamble to prepend to each prompt')

    args = parser.parse_args()

    output_file = f"{args.input_file.rsplit('.', 1)[0]}_tuning_data.{args.output}"
    data = []

    try:
        with open(args.input_file, 'r', encoding='utf-8') as myfile:
            pending = {}
            for line in myfile:
                if line.isspace() or not line.strip():
                    continue

                try:
                    detected_lang = detect(line.strip())
                except LangDetectException:
                    continue  # Skip this line if language detection fails

                markdown_line = convert_to_markdown(line.strip())

                # Prepend the prompt to input_text if provided
                if detected_lang == args.lang1:
                    text_with_prompt = f"{args.prompt} {markdown_line}" if args.prompt else markdown_line
                    pending['input_text'] = text_with_prompt
                elif detected_lang == args.lang2:
                    pending['output_text'] = markdown_line

                if 'input_text' in pending and 'output_text' in pending:
                    # Ensuring correct order in JSON output based on argument order
                    ordered_row = {'input_text': pending['input_text'], 'output_text': pending['output_text']}
                    data.append(ordered_row)
                    pending.clear()

        if args.output == 'csv':
            write_csv(data, output_file)
        else:
            write_json(data, output_file)

        print(f"Successfully created tuning data file: {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

