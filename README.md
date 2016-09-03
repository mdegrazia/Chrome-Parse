# Chrome-Parse
Parse Chrome History and Downloads into TSV or TLN format

Usage:

To parse the history into tsv format:
chrome_parse.py -r -f C:\Users\<USER>\AppData\Local\Google\Chrome\User Data\Default\History >> chrome_history.tsv

To parse the downloads into tsv format:
chrome_parse.py -d -f C:\Users\<USER>\AppData\Local\Google\Chrome\User Data\Default\History >> chrome_history.tsv

To parse the history and downloads into TLN format:
chrome_parse.py -d -r -d -t C:\Users\<USER>\AppData\Local\Google\Chrome\User Data\Default\History >> chrome_history_tln.txt
