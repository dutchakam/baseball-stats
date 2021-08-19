import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import scraperfunctions as sf


def batting_stats_scrape():
    """scrapes data from ESPN website for top batters in the
    league based on user input and organizes it into a dataframe"""

    pd.set_option('display.width', 320)
    pd.set_option('display.max_columns', 20)

    num_pages = sf.get_user_input()
    url = 'https://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2021'
    headers = {'user-agent': 'Chrome/91.0.4469.4'}
    html_req = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_req.text, 'html.parser')

    df = sf.create_dataframe(soup, 'td', 2, 17)

    for page in range(1, num_pages, 50):
        new_url = sf.create_url(page, url)
        html_req = requests.get(new_url, headers=headers)
        soup = BeautifulSoup(html_req.text, 'html.parser')
        players = soup.findAll('tr', {'class': re.compile('row player-10-')})
        for i in range(len(players)):
            player_data = [data.text for data in players[i].findAll('td')[1:]]
            df = df.append(dict(zip(df.columns, player_data)), ignore_index=True)

    df.index += 1

    num_cols = df.columns[1:]
    sf.to_numeric(df, num_cols)

    # insert a Singles column
    df.insert(6, '1B', df.H - (df['2B'] + df['3B'] + df['HR']), allow_duplicates=False)

    # insert Slugging Percentage
    df['SLG'] = round((df['1B'] + (df['2B']*2) + (df['3B']*3) + (df['HR']*4)) / df['AB'], 3)

    return df


if __name__ == "__main__":
    main_df = batting_stats_scrape()
    print(main_df)






