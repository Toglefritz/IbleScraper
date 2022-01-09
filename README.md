<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/iblescraper_logo.PNG?raw=true" alt="IbleScraper logo" width="300"/>

# IbleScraper
A Python web scraper to extract lists of projects from Instructables.com category/channel pages.

## Introduction  :wave:
Do you think that we can use machine learning (GPT-3) to generate ideas
for new project on Instructables? Let's find out.

This repository contains a script. The purpose of this script is to get the conrtent of category/channel pages from Instructables and scrape those pages to obtain a dataset of projects that can be used in a machine learning system to generate ideas for new projects that are similar (in whatever way the ML model figures out) to the projects in the list.

The script will prompt you to select a category and a channel and then it will gather a list of Instructable titles from the appropriate category/channel page (for example [https://www.instructables.com/circuits/robots/projects/](https://www.instructables.com/circuits/robots/projects/)).

## Using IbleScraper  :rocket:
Using IbleScraper is really easy. First of all, the only setup you need to do before you start scraping to your heart's content ([ethically though](https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01)) is to [install Python](https://www.python.org/downloads/).

With Python installed, pop open your favorite terminal program (pictured here is the bog standard Windows Command Prompt) and enter the command ```IbleScraper.py```. You'll be greeted by the IbleScraper running in a new terminal window.

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/iblescraper_screenshot_1.PNG?raw=true" alt="IbleScraper screenshot" width="500"/>

Then, following along with the instructions, enter in your desired category from the list. Note that capitalization matters here (making it not matter is a future enhancement).

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/iblescraper_screenshot_2.PNG?raw=true" alt="IbleScraper screenshot" width="500"/>

The tool will populate a list of channels under the category you just selected. So enter one of those as well (capitalization still matters).

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/iblescraper_screenshot_3.PNG?raw=true" alt="IbleScraper screenshot" width="500"/>

Once you enter a channel, IbleScraper will get right down to business gathering a list of project titles under your selected category/channel pair. Once it is done (and it should only take a moment), the script will create a text file in the same directory as the script containing the list of titles.

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/iblescraper_screenshot_4.PNG?raw=true" alt="IbleScraper screenshot" width="500"/>

## How Does IbleScraper Work?  :microscope:
At a high level, the IbleScraper script has four major parts:
1. Prompt the user (that's you probably!) to enter a category and then a channel
2. From the category/channel combination, get the content of the corresponding page on Instructables.com
3. Scrape the resulting HTML content to gather a list of project titles
4. Output this list of titles in a text file

### Chaper 1: Getting user input
The first step in the script is to get two inputs from the user: an Instructables category and a channel within that category. The script has a dictionary that contains a list of channels keyed by categories. This dictionary drives the user input portion:

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/code_screenshot_1.PNG?raw=true" alt="IbleScraper code" width="500"/>

For the category input question, the script builds an input text string by looping through the dictionary and getting all the keys (which are the categories). The script places a new line after each category name to make a vertical list. Then this prompt is presented to the user with the input() method.

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/code_screenshot_2.PNG?raw=true" alt="IbleScraper code" width="500"/>

So then the user inputs some text and the script makes sure that the text entered is one of the available categories. It does not make sense to accept any other input because that will just result in a 404 response from Instructables.com later on (more on that below).

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/code_screenshot_3.PNG?raw=true" alt="IbleScraper code" width="500"/>

After receiving a valid input for the category prompt, the script moves on to asking for a channel within that category. The process for presenting the channel list is very similar to the one used for the category input but building the input prompt is a little more involved. Because there are quite a few channels within each category, the channels are presented in two columns. A single one would just be long an unwieldy. So, the script takes the list of channels under the selected category (from the dictionary above) and creates two lists, left_column and right_column.

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/code_screenshot_4.PNG?raw=true" alt="IbleScraper code" width="500"/>

Now here comes the tricky part. We would like the right column to be aligned. In other words, the first letter of each channel in the right column should be right on top of the other. If we were to just add, for example, eight spaces after each item in the left column, the right column would not be aligned because the channels are all different lengths. It would end up like this:

```
   Apple        Arduino
   Art        Assistive Tech
   Audio        Cameras
   Clocks        Computers
   Electronics        Gadgets
   Lasers        LEDs
   Linux        Microcontrollers
   Microsoft        Mobile
   Raspberry Pi        Remote Control
   Reuse        Robots
   Sensors        Software
   Soldering        Speakers
   Tools        USB
   Wearables        Websites
   Wireless
```

That just looks bad. Therefore, we need to make the space between the left and right column in each row different depending upon how long the channel name in the left row is.

Here's how we do this. For each row in the list, we want the right column to start on character #26. Therefore, if the item in the left column is 10 characters long, we need to add 16 spaces between that item and the one in the right column next to it. If, in the next row, the item in the left column is 20 characters long, we need to add 6 spaces before the item in the right column. This might take a moment to ponder but here's how it looks in the code.

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/code_screenshot_5.PNG?raw=true" alt="IbleScraper code" width="500"/>

After this column business, the rest of the process is the same as it was for the category selection. We make sure that the text the user enters is within the list of channels.

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/code_screenshot_6.PNG?raw=true" alt="IbleScraper code" width="500"/>

### Chaper 2: Get the page from Instructables.com
Once the user has selected a category and channel, the next step is to obtain the HTML markup for the corresponding page. The category/channel pages on Instructables.com look like this:

```https://www.instructables.com/<category>/<channel>/projects/```

So, we build the URL string and then perform a simple GET REST request to that URL to get the content of that page.

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/code_screenshot_7.PNG?raw=true" alt="IbleScraper code" width="500"/>

### Chaper 3: Parse the HTML
With the HTML document in hand, the next step is to parse out the project titles. To parse the HTML, we will use a tool called [BeautifulSoup]("https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/") (which is an amazing name). We will start by creating a BeautifulSoup object from the HTML.

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/code_screenshot_8.PNG?raw=true" alt="IbleScraper code" width="500"/>

The title for each Instructable is in an ```<a>``` element with the class, "ible-title." So, we want to get a list of these on the page. Beautiful Soup has a couple powerful methods for getting targeted information from the HTML document. In this case we will use the find_all method to get all of the anchor tags with the ible-title class.

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/code_screenshot_9.PNG?raw=true" alt="IbleScraper code" width="500"/>

So then we will loop through the list of all the ible-title elements and get the content from each one. We will assemble the titles into another list that we will work on exporting to an output file in just a moment.

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/code_screenshot_10.PNG?raw=true" alt="IbleScraper code" width="500"/>

### Chaper 4: Save the Results
For the final step of the scraping process, we will save the Instructable titles for the category/channel that we just gathered to a text file. The content of this text file can then be provided to the machine learning system that will be used to generate new ideas for Instructables like the ones in the list.

Saving the results to a file is quite easy. We simply loop through the list of titles and add each one to a file. Python will automatically handle creating the file.

<img src="https://github.com/Toglefritz/IbleScraper/blob/main/images/code_screenshot_11.PNG?raw=true" alt="IbleScraper code" width="500"/>