Gistify is an automatic text summarization tool developed by Rupayan Basu. It works best with news/magazine  articles and non-fiction pieces in general.

Installation:

Mac users can directly run gistify from the command line using the provided gistify.exe file. Download only gistify.exe from the repo, and when using gistify from the command line, run ./gistify instead of ./gistify.py

For other operating systems please follow these instructions - 
To install gistify, make sure you have python and perl installed first. 
Download files gistify.py and install.pl from the repo. 
Run the following commands from the directory containing the files:
$sudo ./install.pl

You are now ready to run gistify!

Using Gistify:

To produce the summary of a text article in sample.txt, run the command below. Gistify produces the summary of the article as well as the counts:
$./gistify.py ­-i sample.txt

To see the original text article with the sentences selected for the summary highlighted in blue, run the following: 
$./gistify.py ­-i sample.txt -­p

Gistify uses a default threshold value of 3 to determine similarity between two sentences. This threshold can be changed with the ­-s option as follows (higher threshold values result in shorter summaries):
$./gistify.py ­-i sample.txt ­-s 4

To compare gistify’s summary with a gold standard summary, use the ­-t <testfile> option as follows: 
$./gistify.py ­-i sample.txt -­t test.txt

For siggestions/feedback please write to 
Rupayan Basu < rb3034 at columbia dot edu >

