# developed to source KT website for specific search term
# By Olivia Fabreschi 11 March 2023

import requests
from bs4 import BeautifulSoup
import re
import csv
# Example url for nodes: https://kt.cern/node/4577
# 4930 = max number of nodes on site as of March 2023
# 3422 = broken node

# input the word you want to search the website for
searched_word = input("Enter word you want to search, not case sensitive: ").strip()

# min node nr -> 1200 if you want to search whole website
nodeNumber = 3421
# max node nr -> 5000
nodeNumberMax = 3500

# lists to add
word_list = []
node_list = []
url_List = []
sentence_list = []
fullList = []

for nodeNumber in range(nodeNumber, nodeNumberMax+1):
    try:
        print(nodeNumber)
        url = f"https://kt.cern/node/{nodeNumber}"
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")
        # Find Elements by Class Name and Text Content
        # This code finds all items where the contained string matches the search word term exactly.
        pattern = re.compile('.*{0}.*'.format(searched_word), flags=re.IGNORECASE)
        items = soup.body.find_all(string=pattern, recursive=True)
        # Find all <p> elements that contain the searched word
        if len(items) != 0:
            # if finding all paragraphs:
            paragraphs = soup.find_all("p")
            # finding and printing sentences mentioning the word
            for p in paragraphs:
                sentences = p.find(string=pattern)
                if sentences is not None:
                    print(sentences)
                    # sentence list
                    sentence_list.append(sentences)
                    node_list.append(nodeNumber)
                    # adding url to list
                    url_List.append(url)
                    #     add searched name to list
                    word_list.append(searched_word)
            # adding node numbers to list to be able to find them

        # combining lists
        fullList = list(zip(node_list, url_List, word_list, sentence_list))

    except:
        pass


print(fullList)
# open a file for writing in CSV format
with open('search_word_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # write the header row
    writer.writerow(['Node Number', "link to page", "search word", "sentence"])

    # write each tuple as a row in the CSV file
    for row in fullList:
        writer.writerow(row)