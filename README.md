# WordListMaker
A Python application designed for making Japanese vocabulary pdfs.

## Functionalities:
This is a Python application that offers the following functionalities:
* Converting Anki decks to Excel files.
* Conversions between PDF and Excel files.
* Removing Katakana words from Japanese Vocabulary study lists.
* Shuffling the rows in an Excel file.
* Generating an Anki deck (Work in Progress).
* Removing a list of entries from a Vocabulary Excel file.
* Removing entries marked in a pdf using this tool.
* Automaticly shuffling and generating a new pdf after removing words.
  
## How to Use:
The purpose of this application is to create Japanese vocabulary lists in PDF format, excluding words that have already been memorized. Randomized shuffling of the list can enhance the learning process. Additionally, checkmarks can be added to the newly created PDF to facilitate the removal of memorized words.

## How to Run:
To run this application, execute the "WordListMaker.py" file.
I did not make a build of this application because this unfortunately, made the font of the created pdf's unreadable.

## Disclaimer:
Conversion of pdf files has only been tested using the Japanese N3 level vocabulary PDF from the [Tanos](https://www.tanos.co.uk/jlpt/jlpt3/vocab/VocabList.N3.pdf) website.

## API_KEY:
If you make use of the generate senteces feature be sure to put your deepseek API key in a textfile in the API_KEY folder.
