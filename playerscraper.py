import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import requests
import scraperfunctions as sf
import statsscraper as ss


def get_batting_data():
    """Runs the batting stats scrape function from the stats_scraper.py file
    and returns the dataframe"""

    pd.set_option('display.width', 500)
    pd.set_option('display.max_columns', None)
    batting_data = ss.batting_stats_scrape()
    print(batting_data)
    return batting_data


def player_data_scrape(batting_data):
    """scrapes data on individual players based on user input and organizes it into a dataframe"""

    pd.set_option('display.width', 500)
    pd.set_option('display.max_columns', None)

    names_list = [name.replace('.', '').lower() for name in batting_data['PLAYER']]

    player = list(input('Enter the name of a player whose stats you would like to see:\n').lower())
    player_name = [name for name in names_list if sf.same_name(player, name, 0.8)][0].strip()

    url = 'https://www.baseball-reference.com/players/'
    headers = {'user-agent': 'Chrome/91.0.4469.4'}

    player_url, final_player_name = sf.create_player_url(player_name, url, headers)

    html_req = requests.get(player_url, headers=headers)
    soup = BeautifulSoup(html_req.text, 'html.parser')
    new_cols = soup.findAll('p')
    if 'Pitcher' in new_cols[0].text:
        df = sf.get_pitcher_data(soup)
    else:
        df = sf.get_non_pitcher_data(soup)

    return df, final_player_name


def plt_subplots(df, name):
    """uses matplotlib and seaborn libraries to plot line graphs for individual player data.
    Plots have different data based on player's position"""

    df = df.set_index('Year')

    if 'P' in list(df['Pos']):
        titles = [f'{name}: Amount Played', f'{name}: Pitching Stats']
        df_graph1 = df[['W', 'L', 'G', 'GS', 'GF', 'IP']]
        df_graph2 = df[['H', 'R', 'ER', 'HR', 'BB', 'IBB', 'SO']]
    else:
        titles = [f'{name}: Batting Percentages', f'{name}: At Bats, Hits, and Runs']
        df_graph1 = df[['BA', 'OBP', 'SLG', 'OPS']]
        df_graph2 = df[['G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO']]
    df_to_plot = [df_graph1.columns, df_graph2.columns]

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes = axes.flatten()

    for i, j, k in zip(df_to_plot, axes, titles):
        sns.lineplot(data=df[i], ax=j)

        j.set_title(k)
        j.set_xlabel('Year')

    plt.tight_layout()
    plt.show()


def run_on_while():
    """Runs the individual player scraping program until the user chooses to exit the program"""

    batting_data = get_batting_data()

    run_player_data_scrape = input('Would you like to get data on a specific player '
                                   'from this dataframe? (yes/no)\n').lower()

    while run_player_data_scrape != 'no':
        main_df = player_data_scrape(batting_data)
        print(main_df[0], '\n')
        plt_subplots(main_df[0], main_df[1])
        run_player_data_scrape = input('Would you like get data on another player? (yes/no)\n').lower()

    print('Farewell!\n\n')


if __name__ == "__main__":
    run_on_while()



