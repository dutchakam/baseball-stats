# baseball-stats
Scrapes batting data from ESPN for top batters in the league. Then gives the option to more closely analyze data on individual players

Libraries used:
  -BeautifulSoup
  -Pandas
  -Requests
  -Re
  -Sys
  -Matplotlib
  -Seaborn
  -Difflib
  -Unicodedata
  
scraperfunctions.py
  -contains functions used in both statsscraper.py and playerscraper.py
  
statsscraper.py
  -scrapes the ESPN website to compile a Pandas DataFrame with data on top batters in the MLB
  -each page on this site shows 50 players
  -The number of rows in the DataFrame will always be a multiple of 50 until you reach the last page on the website
  
playerscraper.py
  -uses the DataFrame produced by statsscraper.py as a list from which the user can select individual players and view data on that player's career
  -player data is compiled into a DataFrame
  -numerical data is presented in 2 graphs using matplotlib and seaborn
  -The accuracy of this data is based on a very weird method for constructing urls on baseball-reference.com which sometimes doesn't follow it's own rules
    -for instance: if you choose to see data on Yuli Gurriel, the program will error and exit, because they misspell the abbreviation of his name in the url, either on accident or     on purpose, I cannot say
    -needless to say, I have not found a solution to this problem yet
    

Created using:
  -Python v3.8
  -PyCharm
