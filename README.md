# epub-ocr-and-translate

### An in-progress set of tools for creating epubs in multiple languages

Scripts to scan a PDF, auto-translate, process, and create epub and PDF output. Getting the dependencies in order can be tricky (a working image can be obtained via ``docker pull jenh/eoat:v2
`` -- apologize for the size, but it's got all of texlive inside...).

## Dependencies:
- Python, most scripts have been tested with 2.7 and 3.6; some of the onmt-helper scripts require Python 3.6. Non-built-in modules used include: google.cloud guess_language pycountry. guess_language won't detect properly unless you also install pyenchant (Fedora or Ubuntu packages are fine) and guess-language-spirit. requirements.txt shows my EC2 instance's pip freeze output
- ImageMagick (also, open /etc/ImageMagick-6/policy.xml and change the "rights" for PDF from "none" to "read|write")
- poppler-utils
- tesseract
- For translation, if using Google Translate, Google Translate API (`pip install gcloud google-cloud-translate` with GOOGLE\_APPLICATION\_CREDENTIALS in your env) and Python module or [translate-shell](https://github.com/soimort/translate-shell). If using Amazon Translate, the latest version of boto3 with API and region configured (`aws configure`).
- texlive with xetex: Recommend installing the entire CTAN distribution (i.e., not using yum or apt-get but using the instructions from https://www.tug.org/texlive/quickinstall.html) and do this *before* installing pandoc
- pandoc 2.8
- ebook-viewer (optional; to view output)
- For LaTeX, applicable language packs (for example, you'll need to `sudo apt install texlive-lang-cyrillic` for russian, `texlive-lang-spanish` for Spanish, etc)
- epubcheck & kindlegen (optional, if you're planning on generating Kindle deliverables)

## Quick Start

1. Clone the project: 
  
   git clone https://github.com/jenh/epub-ocr-and-translate

2. Install the tools: 
  
   cd epub-ocr-and-translate && sudo sh install.sh

3. Create a working directory:

   mkdir my\_working\_directory

4. Copy the PDF you want to process into your working directory:

    cd my\_working\_directory && cp /path/to/my/input.pdf . 

5. Run eoat-tool ocr:

    eoat-tool ocr input.pdf eng 

    (where eng is the [three letter language code](https://www.loc.gov/standards/iso639-2/php/code_list.php) of your source doc).

6. Translate the OCRed output:

    eoat-tool trans -i output-from-step-five.txt -s en -t fr

7. Split the translated files into chapter files:

    eoat-tool split -i output-from-step-six.2lang.md -d "CHAPTER"

8. Run the make tool to add metadata and create Makefiles to be used for PDF and epub creation:

   eoat-tool make

9. Edit variables.yaml with your intended metadata.

10. Build your deliverables:

    eoat-tool build fr 

    (where fr is the two letter language code of the translation you want to epub/PDF)

## Standard workflow:

1. OCR a PDF with `eoat-ocr.sh`

    Given a PDF file, OCR and clean it up a little. Requires ImageMagick, tesseract, pdfinfo/pdfseparate. 

    **Usage**: 

    `sh eoat-ocr.sh filename.pdf eng`

    where `eng` is the three letter language code of the source document. See list [here](http://www.loc.gov/standards/iso639-2/php/code_list.php). Source language document is very important! Note that this may take awhile, depending on the number of pages in your PDF. 

2. Translate a file with `eoat-trans.py`

    `eoat-trans.py` uses Google's Translate API, which costs $, [`translate-shell`](https://github.com/soimort/translate-shell), which is awesome, but you can and will get blocked by translation engines, so it's not great for large texts (but you *can* specify google, bing, yandex, etc), or Amazon Translate (free for 2M characters, then $). WARNING! translate-shell with many of the engines, even Google, can be unreliable because engines WILL block you after a certain number of characters. For important work, Google Cloud API is still unfortunately your best bet, though pricey, like $10/million characters. You can also now use OpenNMT Simple REST Server as an input, the script assumes it's running locally if you set the engine to opennmt.

    **Usage for eoat-trans.py:** `python eoat-trans.py -i source_text_file -s two-letter-source_lang -t two-letter-target_lang [-e trans|gcloud] [-w wait_seconds]`


    -e is optional, uses translate-shell by default. There's a default two second wait between translation requests, you can change this with -w.

3. Cut files into individual markdown files for each chapter using ``eoat-split.py``
   
    **Usage:** 
    
    `python eoat-split.py -i filename.txt -d CHAPTER` 
    
    (where CHAPTER is the chapter-delimiter; accepts UTF-8, so you can use other languages where necessary. For example, if your source text is Russian, you could use "Глава"). 

4. Edit markdown output as needed. This is probably the hardest part. Good luck! You may want to skip this and run the other steps to see how much more post-processing work you've got to do. 

5. Build a Makefile that will generate your epub and PDF files from your Markdown source with `eoat-make.py`

    Creates a make file that will output epub and PDF, gathering all *.md files in the current directory. Requires xetex and pandoc. And ebook-viewer if you want to pop open the output. You should only have to run this once; if you run it again at some point, make sure you've deleted all autogenerated *lang*md files created using step 6.

    **Usage:** `python eoat-make.py`

6. Create PDF and epub files using `eoat-build.sh`

    **Usage:** `sh eoat-build.sh two_letter_lang`

    `eoat-build.sh` requires `eoat-printlang.py`, which can also be used in standalone mode. It takes a master file that contains two languages, like:

        Это по русски

        This is in English

        Это по русски

        This is in English

    And exports the language you specify. Usage is ``python eoat-printlang.py input_file two_letter_lang_code``

## Other scripts:

- eoat-cleanup.sh: The file cleanup components from eoat-ocr.sh without the ocr part.

- eoat-corpusclean.py: Utility to clean lines that match a provided regex from two language corpus training files. Useful if you're plugging OpenNMT into your system.

- eoat-expandlang.py: Utility to feed back a babel-friendly language package name when provided a two-letter language code (used by eoat-build). 

- eoat-install.sh: Installs these scripts to /opt and symlinks to /usr/bin so that you can run from any working directory.

- eoat-printlang.py: Given a filename and language code, searches file for language that matches the language code and exports into a new file. Used by eoat-build.

- eoat-process.sh: A basic translator in bash, just runs translate-shell. For translations, eoat-trans.py has more extensibility and features, but sometimes you just need to do a quick run.

- eoat-tool.py: Wrapper script for the basic core building tools.

- eoat-uninstall.sh: Uninstalls eoat-tools from /opt/ and unlinks eoat utilities /usr/bin.

- onmt-helpers directory: Assistive scripts that may help if you're using your own translation engine with OpenNMT-py. 
