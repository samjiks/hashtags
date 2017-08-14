# Create Hashtag 

## Create Hashtags

Hashtags is sentence finder with most common occuring words

## Getting Started

These instructions will get you a copy of the project up and running on
your local machine for development and testing purposes.

## Prerequisites

Requires Python 3 and above. While developing I used python 3.4. 

Developed on MAC, If using Windows, when manipulating paths for full
document is not tested.

## Installing

Step 1: Make the virtual environment with python3.4

virtualenv .venv

Step 2: Activate the virtual environment

pip install -r requirements

## Running the program

Command: python main.py -a 5 -f -o output.json -i

-a n This takes the first 'n' most common words 
-f This will filter out all noise words such as punctuation, articles
-o This is required to output hash tag sentences to a txt file

### Output

+----------+------------+------------------------------------------------------------------------------------------------------+
| Word(#)  | Documents  |                                    Sentences containing the word                                     |
+----------+------------+------------------------------------------------------------------------------------------------------+
| American | doc1.txt,  | where North, South, East and West come together that I was reminded of the essentia decenc          |
|          | doc2.txt,  | y of the American people - where I came to believe that through this decency, we can build a moreho |
|          | doc3.txt,  |                                            peful America.                                           |
|          | doc4.txt,  |                                                                                                     |
|          | doc5.txt,  |                        his millennium together, as one people - as Americans.                       |
|          |  doc6.txt  |                                                                                                     |
|          |            |       It's a promise that says the market should reward drive and innovation and generate grow      |
|          |            | th, but that businesses should live up to their responsibilities to create American jobs, look outf |
|          |            |                       or American workers, and play by the rules of the road.                       |
|          |            |                                                                                                     |
|          |            |                             It should ensure opportunity not just for t                             |
| people   | doc1.txt,  | In the face of a politics that's shut you out, that's told you to settle, that's divided us for too |
|          | doc2.txt,  | long, you believe we can be one people, reaching for what's possible, building that more perfectuni |
|          | doc3.txt,  |                                                 on.                                                 |
|          | doc4.txt,  |                                                                                                     |
|          | doc5.txt,  |   I joined with pastors and lay-people to deal with communities that had been ravaged by plant cl   |
|          |  doc6.txt  |                                               osings.                                               |
|          |            |                                                                                                     |
|          |            |     I saw that the problems people faced weren't simply local in nature - that the decision to      |
|          |            | close a steel mill was made by distant executives; that the lack of textbooks and computers inschoo |
|          |            | ls could be traced to the skewed priorities of politicians a thousand miles away; and that when ach |
|          |            |          ild turns to violence, there's a hole in his heart no government could ever fill.             
     
## Help

Command: python main.py -h 
usage: main.py [-h] [-a FIRST] [-f] [-v] -o OUTPUT [-d DIRECTORY] [-i] [-fdp]

optional arguments:
  -h, --help            show this help message and exit
  -a FIRST, --first FIRST
                        Get the first few common words, Default is 5
  -f, --filter          Filter out all punctuations, articles and
   any other
                        unnecessary words
  -v, --verbose         Increase logging level to Debug
  -o OUTPUT, --output OUTPUT
                        Output JSON
  -d DIRECTORY, --data-dir DIRECTORY
                        Directory to which the files to be searched,
                         Default
                        is project's data directory
  -i, --display         View the output in tabular format
  -fdp, --full-document-path
                        Get the full Document path
