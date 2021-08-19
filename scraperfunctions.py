from bs4 import BeautifulSoup
import requests
import difflib
import pandas as pd
import unicodedata
import re
import sys


def get_user_input():
    """Gets user input for how many players' stats to scrape"""
    valid_input = False
    while not valid_input:
        user_input = input("How many players' stats would you like to see?\n")
        try:
            user_input = int(user_input)
            if user_input < 75:
                user_input = 51
                valid_input = True
            else:
                user_input = my_round(user_input)
                valid_input = True
        except ValueError:
            print('Invalid entry. Please enter a number.\n\n\n')
            valid_input = False
    return user_input


def my_round(user_input, base=50):
    """Rounds the user input to nearest multiple of 50"""
    return base * round(user_input / base) + 1


def create_url(page, url):
    """creates a url based on how many players' stats being scraped"""
    if page < 51:
        return url
    else:
        return url + f'/start/{page}'


def create_player_url(player_name, url, headers):
    """Takes apart a player's name and builds a url with it. Since the website uses abbreviated names in the url,
    there are often multiple players with similar urls. Also converts unicode characters to ascii for accuracy"""
    split_name = [name.lower() for name in player_name.split()]
    initial = split_name[1][0]
    name_abbrev = split_name[1][:5] + split_name[0][:2]
    url_ending = f'{initial}/{name_abbrev}01.shtml'
    url += url_ending
    # check to make sure we got the correct player
    html_req = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_req.text, 'html.parser')
    try:
        check_name = soup.find('h1', {'itemprop': 'name'}).text.strip().replace('.', '')
    except AttributeError:
        print(f'Unable to find correct url for player: '
              f'{" ".join([name.capitalize() for name in player_name.split()])}\n')
        sys.exit()
    check_name_modified = unicodedata.normalize('NFKD', check_name).encode('ascii', 'ignore').decode().lower()
    # if incorrect player, transform the url
    page = 1
    while check_name_modified != player_name:
        url = url.replace(f'0{page}', f'0{page + 1}')
        html_req = requests.get(url, headers=headers)
        soup = BeautifulSoup(html_req.text, 'html.parser')
        check_name = soup.find('h1', {'itemprop': 'name'}).text.strip().replace('.', '')
        check_name_modified = unicodedata.normalize('NFKD', check_name).encode('ascii', 'ignore').decode().lower()
        page += 1
    print(check_name, '\n', url)
    return url, check_name


def same_name(player, names_list, ratio):
    """finds names from a list that are similar to the entered name
    using the ratio method from the difflib library."""
    return difflib.SequenceMatcher(None, player, names_list).ratio() > ratio


def create_dataframe(soup, tag, idx1, idx2):
    """creates a dataframe with the appropriate column names using the player's url"""
    new_cols = soup.findAll(tag)
    my_cols = [col.text for col in new_cols[idx1:idx2]]
    df = pd.DataFrame(columns=my_cols)
    return df


def to_numeric(df, cols):
    """converts string values to numerical in appropriate columns"""
    for col in cols:
        df[col] = pd.to_numeric(df[col])


def get_non_pitcher_data(soup):
    """If the player whose name was entered is a pitcher,
    this function will create a dataframe with appropriate size
    and column names"""
    df = create_dataframe(soup, 'th', 0, 29)

    player = soup.findAll('tr', {'id': re.compile('batting_standard')})
    for i in range(len(player)):
        player_data = [data.text for data in player[i].findAll('td')[:-1]]
        year_data = [data.text for data in player[i].findAll('th', {'data-stat': 'year_ID'})][0]
        player_data.insert(0, year_data)
        df = df.append(dict(zip(df.columns, player_data)), ignore_index=True)

    num_cols = df.columns[4:28]
    to_numeric(df, num_cols)

    return df


def get_pitcher_data(soup):
    """For any player who is not a pitcher,
    this function will create a dataframe with appropriate size
    and column names"""
    df = create_dataframe(soup, 'th', 0, 34)

    player = soup.findAll('tr', {'id': re.compile('pitching_standard')})
    for i in range(len(player)):
        player_data = [data.text for data in player[i].findAll('td')[:-1]]
        year_data = [data.text for data in player[i].findAll('th', {'data-stat': 'year_ID'})][0]
        player_data.insert(0, year_data)
        df = df.append(dict(zip(df.columns, player_data)), ignore_index=True)

    df['Pos'] = 'P'
    num_cols = df.columns[4:-1]
    to_numeric(df, num_cols)

    return df



