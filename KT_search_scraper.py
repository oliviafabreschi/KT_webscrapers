# developed to source KT website for specific search term
# By Olivia Fabreschi 11 March 2023

import requests
from bs4 import BeautifulSoup
import re
import csv
# Example url for nodes: https://kt.cern/node/4577
# 1250 = min number for relevant content on site as of April 2023
# 4940 = max number of nodes on site as of April 2023
# 3422 = broken node

# input the word you want to search the website for
searched_word = input("Enter word you want to search, not case sensitive: ").strip()

# min node nr: to be changed based on desired search range
nodeNumber = 3907
# max node nr: to be changed based on desired search range
nodeNumberMax = 4200

# lists to add
word_list = []
node_list = []
url_List = []
sentence_list = []
fullList = []
urlCategory = []
urlNameAlt = ""


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
            try:
                urlNameAlts = soup.head.find_all("link", rel="alternate")
            except:
                pass
            # getting the alternative url link for clearer page name
            for loc in urlNameAlts:
                # urlNameAlt = loc['href'].split("/")[1:-1]  # extract the href attribute value
                urlNameAlt = loc['href'][:]  # extract the href attribute value
                print(urlNameAlt)
                # append urlCategory
                urlCategory.append(urlNameAlt)
            # if finding all paragraphs:
            paragraphs = soup.find_all("p")
            # finding and printing sentences mentioning the word
            for p in paragraphs:
                sentences = p.find(string=pattern)
                if sentences is not None:
                    print(sentences)
                    # sentence list
                    sentence_list.append(sentences)
                    # node list
                    node_list.append(nodeNumber)
                    # adding url to list
                    url_List.append(url)
                    # add searched name to list
                    word_list.append(searched_word)


        # combining lists
        fullList = list(zip(node_list, url_List, word_list, sentence_list, urlCategory))

    except:
        pass


print(fullList)
# open a file for writing in CSV format
with open('search_word_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # write the header row
    writer.writerow(['Node number', "link to page", "searched word", "sentence extract", "urlCategory"])

    # write each tuple as a row in the CSV file
    for row in fullList:
        writer.writerow(row)