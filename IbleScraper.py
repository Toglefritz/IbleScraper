# IbleScraper
# Dataset Generation Web Scraper For Instructables.com Projects
# by Toglefritz (https://www.instructables.com/member/Toglefritz/)

# Do you think that we can use machine learning (GPT-3) to generate ideas
# for new project on Instructables? Let's find out.

# The purpose of this script is to get the conrtent of category pages from
# Instructables and scrape those pages to obtain a dataset of Instructables
# that can be used in a machine learning system to generate ideas for 
# projects that are similar (in whatever way the ML model determines) to 
# the Instructables in the list.

from requests_html import _URL, HTMLSession
from bs4 import BeautifulSoup

print("  ___ _     _      ____                                 ")
print(" |_ _| |__ | | ___/ ___|  ___ _ __ __ _ _ __   ___ _ __ ")
print("  | || '_ \| |/ _ \___ \ / __| '__/ _` | '_ \ / _ \ '__|")
print("  | || |_) | |  __/___) | (__| | | (_| | |_) |  __/ |   ")
print(" |___|_.__/|_|\___|____/ \___|_|  \__,_| .__/ \___|_|   ")
print("                                       |_|              ")
print("\n")

# Instructables channels and their channels
# TODO add All Channels options
channels = {
    "Circuits": ["Apple", "Arduino", "Art", "Assistive Tech", "Audio", "Cameras", "Clocks", "Computers", "Electronics", "Gadgets", "Lasers", "LEDs", "Linux", "Microcontrollers", "Microsoft", "Mobile", "Raspberry Pi", "Remote Control", "Reuse", "Robots", "Sensors", "Software", "Soldering", "Speakers", "Tools", "USB", "Wearables", "Websites", "Wireless", ""],
    "Workshop": ["3D Printing", "Cars", "CNC", "Electric Vehicles", "Energy", "Furniture", "Home Improvement", "Home Theater", "Hydroponics", "Knives", "Laser Cutting", "Lighting", "Metalworking", "Molds & Casting", "Motorcycles", "Organizing", "Pallets", "Repair", "Science", "Shelves", "Solar", "Tools", "Woodworking", "Workbenches"], 
    "Craft": ["Art", "Books & Journals", "Cardboard", "Cards", "Clay", "Costumes & Cosplay", "Digital Graphics", "Duct Tape", "Embroidery", "Fashion", "Felt", "Fiber Arts", "Gift Wrapping", "Jewelry", "Knitting & Crochet", "Leather", "Mason Jars", "No-Sew", "Paper", "Parties & Weddings", "Photography", "Printmaking", "Reuse", "Sewing", "Soapmaking", "Wallets"],
    "Cooking": ["Bacon", "BBQ & Grilling", "Beverages", "Bread", "Breakfast", "Cake", "Candy", "Canning & Preserving", "Cocktails & Mocktails", "Coffee", "Cookies", "Cupcakes", "Dessert", "Homebrew", "Main Course", "Pasta", "Pie", "Pizza", "Salad", "Sandwiches", "Snacks & Appetizers", "Soup & Stews", "Vegetarian & Vegan"], 
    "Living": ["Beauty", "Christmas", "Cleaning", "Decorating", "Education", "Gardening", "Halloween", "Health", "Hiding Places", "Holidays", "Homesteading", "Kids", "Kitchen", "LEGO & K'NEX", "Life Hacks", "Music", "Office Supply Hacks", "Organizing", "Pest Control", "Pets", "Pranks, Tricks, & Humor", "Relationships", "Toys & Games", "Travel", "Video Games"],
    "Outside": ["Backyard", "Beach", "Bikes", "Birding", "Boats", "Camping", "Climbing", "Fire", "Fishing", "Hunting", "Kites", "Knots", "Launchers", "Paracord", "Rockets", "Siege Engines", "Skateboard", "Snow", "Sports", "Survival", "Water"], 
}

# Sorting methods (ordered from highest/most to lowest/least for reach method)
methods = ["Featured", "Recent", "Popular", "Views", "Winners"]

# Ask the user to choose a category
while True:
    categoryPromptText = 'Let\'s start by choosing one of these categories, please:\n'
    # Loop over all the channels and list them in the prompt
    for key in channels:
        categoryPromptText += '   ' + key + '\n'
    categoryPromptText += '\n(type in the category):  '

    categoryChoice = input(categoryPromptText)
    if categoryChoice in channels:
            print('\nYou selected the ' + categoryChoice + ' category. Good choice.\n')
            # If the entry is valid, break from the loop
            break
    else:
        # We will only accept the listed categories
        print('\nPlease select one of the listed categories. Those are all the ones available after all.\n')

# Ask the user to choose a channel for the selected category
while True:
    channelPromptText = 'Now let\'s select a channel from the ' + categoryChoice + ' category:\n'
    # There are a lot of channels so we will list them in two columns
    left = True     # Track which column we are adding to
    leftColumn = []
    rightColumn = []

    # Loop over the channels and put them into two columns
    for key in channels[categoryChoice]:
        if left:
            leftColumn.append(key)
        else:
            rightColumn.append(key)
        left = not(left)    # Switch column

    # Loop through the two columns to build the prompt
    i = 0
    while i < len(leftColumn):
        # Create a space between columns so they all line up
        space = '   '
        x = 0
        # The right column items should all start on the 26th character so we add spaces
        # to any item in the left column under 26 characters to make this true
        while x < (26 - len(leftColumn[i])):
            space += ' '
            x += 1

        channelPromptText += '   ' + leftColumn[i] + space + rightColumn[i] + '\n'
        i += 1

    channelPromptText += '\n(type in the channel):  '

    channelChoice = input(channelPromptText)
    if channelChoice in channels[categoryChoice]:
            print('\nYou selected the ' + channelChoice + ' channel. Nice.\n')
            # If the entry is valid, break from the loop
            break
    else:
        # We will only accept the listed categories
        print('\nPlease select one of the listed channels. This just will not work otherwise.\n')

# Ask the user to select a sorting order for the projects
while True:
    sortingPromptText = 'Next, please select a sorting method for the results (highest/most to lowest/least):\n'
    for method in methods:
        sortingPromptText += '   ' + method + '\n'
    sortingPromptText += '\n(type in the sorting method):  '

    sortingChoice = input(sortingPromptText)
    if sortingChoice in methods:
        if sortingChoice == "Featured":
            print('\nThe results will be sorted from most recently featured to least recently featured.\n')
        elif sortingChoice == "Recent":
            print('\nThe results will be sorted from newest to oldest.\n')
        elif sortingChoice == "Popular":
            print('\nThe results will be sorted in order of popularity.\n')
        elif sortingChoice == "Views":
            print('\nThe results will be sorted in order of views.\n')
        elif sortingChoice == "Winners":
            print('\nThe results will be sorted from most recent winners to least recent winners.\n')
        # If the entry is valid, break from the loop
        break
    else:
        # We will only accept the listed categories
        print('\nPlease select one of the listed sorting methods. I don\'t know how to sort in any other ways.\n')

# Ask the user to input a number of pages to scrape
while True:
    pagesPromptText = 'Finally, how many pages would you like to scrape?\n(enter a number 1-100):  ' 
    pagesChoice = input(pagesPromptText)
    if(int(pagesChoice) >= 1 & int(pagesChoice) < 100):
        print('We will take a look at ' + pagesChoice + ' pages.\nLet\'s get started.\n')
        break
    else:
        print('Please enter a number of pages between 1 and 100.\n')

# This is a list of titles for the Instructables in this category/channel
# This list is essentially the output of the script as it will be written
# directly into the output text file
ibles = [] 

# We will loop to repeat the process for each page
page = 0
while page < int(pagesChoice):
    # Get the content for the current page
    url = 'https://www.instructables.com/' + categoryChoice.lower() + '/' + channelChoice.lower() + '/projects/'
    # Add the sorting choice to the URL (Featured does not add anything though)
    if sortingChoice != "Featured":
        url += sortingChoice.lower() + '/'
    # For pages after page 1, append the page number to the URL
    if page > 1:
        url += ('?page=' + str(page))
    print('Getting projects under ' + categoryChoice + '/' + channelChoice + '.\nURL: ' + url + '\n')  
    session = HTMLSession()
    r = session.get(url)

    # We will scape the website using Beautiful Soup
    soup = BeautifulSoup(r.text, 'html.parser')

    # First get all the project titles for this cateogry/channel
    titles = soup.find_all("a", {"class": "ible-title"})

    # Second, create a list of all these titles
    for title in titles:
        ibles.append(str(title.text))

    # Go to the next page
    page += 1

# Third, create a file containing the output of the scraper (a list of project titles)
fileName = 'iblescraper_' + categoryChoice.lower() + '_' + channelChoice.lower() + '.txt'
with open(fileName, "w", encoding='utf8', errors="ignore") as txt_file:
    for title in ibles:
        txt_file.write(title + "\n")

print('The list of Instructable titles has been saved "' + fileName + '"')

while True:
    print('\nThank you for using IbleScraper. Please come again.\n')
    input('(Press ENTER to exit)')
    break
    