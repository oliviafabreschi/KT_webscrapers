# developed to source KT website for names associated with specific pages
# loops through all pages via nodes
# parses and creates lists for url name, technology title, name associated
# for pages that have a contact name associated with it
# lists combined and then exported to one CSV file
# By Olivia Fabreschi 11 March 2023

import requests
from bs4 import BeautifulSoup
import csv

# Example url for nodes: https://kt.cern/node/4577
# 1250 = min node for active page content
# 4940 = max number of nodes on site as of April 2023


# minimum nr - to be changed
nodeNumber = 4780
# max to search to - to be changed
nodeNumberMax = 4920

# lists to add to
name_list = []
node_list = []
url_List = []
tech_list = []
KTOperPage = []
urlCategory = []
techName = ""
urlNameAlt = ""
nameKTO = ""

#for creating csv files
def makecsv():
    # open a file for writing in CSV format
    with open('KT_name_list.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # write the header row
        writer.writerow(['Node Number', 'KTO Name', "technology name", "link to page", "Page category"])

        # write each tuple as a row in the CSV file
        for row in KTOperPage:
            writer.writerow(row)

#function to get the UrL using beautiful soup
def geturl():

        # finding all url alternative names to get page category via head location
        try:
            urlNameAlts = soup.head.find_all("link", rel="alternate")
        except:
            pass
        for loc in urlNameAlts:

                urlNameAlt = loc['href'].split("/")[3]  # extract the href attribute value
                # append urlCategory
                urlCategory.append(urlNameAlt)

# adding information to lists
def amendlists():
    # initialize urlCategory as an empty list
    # adding url to list
    url_List.append(url)
    # adding node number to list
    node_list.append(nodeNumber)
    # title of page/tech name
    tech_list.append(techName)

# function to get contact name on pages based on contact card location - either in link tag or div tag
def getname(lines):

        try: # finding all contact cards in body location
            div_element = soup.find_all('div', {
                        'class': 'field field--name-field-p-contact-person-full-name field--type-string field--label-hidden field--item'})
            # getting all contacts if it is located in a div element
            if div_element:
                try:
                    for tag in div_element:    #looping through each tag in the div element (kt fund pages)
                        try:
                            nameKTO = tag.string.replace("KT Officer: ", "")
                            print(nameKTO)
                        except:
                            nameKTO = "Undefined"
                            print(nameKTO)
                        name_list.append(nameKTO)

                except Exception as e:
                    print(e)
                    pass
            # if no div tag present for name, looking for a tag (technology pages)
            else:
                try:
                    for line in lines:
                        page_text = line.find("a")
                        if page_text is not None:
                            page_text = str(page_text)
                            nameKTO = page_text.split("/")[2].split('"')[0].replace("-", " ")

                            # fixing bug for certain tags
                            if nameKTO == "1955":
                                nameKTO = "Alessandro Raimondo"
                            print(f"name on page: {nameKTO}")
                            name_list.append(nameKTO)



                        else:
                            if name_list:
                                for nameKTO in name_list:
                                    name_list.append(nameKTO)
                                    break
                except Exception as e:
                    print(e)
                    pass
        except:
            pass

# main loop, iterating over each page based on node number and calling
# all functions for each page
# with try/except for broken pages
try:
    #looping through each page based on node numbers
    for nodeNumber in range(nodeNumber, nodeNumberMax + 1):
        print(nodeNumber)
        url = f"https://kt.cern/node/{nodeNumber}"
        try:
            page = requests.get(url).text
            soup = BeautifulSoup(page, "html.parser")
            # finding all contact cards in body location
            items = soup.body.find_all(class_="component-related_card__content__link")
        except:
            pass

        # if the contact card exist, i.e. if a contact name is associated with the page
        # call function for getting the names based on the contact class field
        getname(items)
        # if there is a contact card, call functions to get other info:
        if len(items) != 0:
            for i in items:
                # call functions
                geturl()
                # get the technology name associated with the contact card
                try:
                    # finding all tech names via title in body location
                    techName = soup.body.find(
                        class_="field field--name-node-title field--type-ds field--label-hidden field--item").find(
                        "h2").get_text().replace('\n', '').strip()
                    print(techName)
                except:
                    techName = "undefined"


                amendlists()
except:
    pass

# printing out results for final reference
print(len(node_list))
print(node_list)
print(len(name_list))
print(name_list)
print(len(tech_list))
print(tech_list)
print(len(url_List))
print(url_List)
print(len(urlCategory))
print(urlCategory)

# combining lists
KTOperPage = list(zip(node_list, name_list, tech_list, url_List, urlCategory))


makecsv()



