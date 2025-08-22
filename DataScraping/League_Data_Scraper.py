##importing all required libraries
from bs4 import BeautifulSoup
import pandas as pd
import requests 
import time
from io import StringIO

all_teams = [] ## list to store all teams

# Add headers to avoid being blocked by source site
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    html = requests.get('https://fbref.com/en/comps/40/Scottish-Premiership-Stats', headers=headers).text ##getting the html from the website
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find_all('table', class_ = 'stats_table')
    
    if not tables:
        print("No tables with class 'stats_table' found. Let's see what's available:")
        all_tables = soup.find_all('table')
        print(f"Found {len(all_tables)} total tables")
        for i, table in enumerate(all_tables[:5]):  # Show first 5 tables
            classes = table.get('class', [])
            table_id = table.get('id', 'No ID')
            print(f"Table {i}: ID='{table_id}', classes={classes}")
        exit(1)
    
    table = tables[0] ##only want the first table, therefore the first index
except requests.RequestException as e:
    print(f"Error fetching main page: {e}")
    exit(1)
except IndexError:
    print("Could not find stats table on the main page")
    exit(1)

links = table.find_all('a') ## finding all links in the table 
links = [l.get("href") for l in links] ##parsing through links
links = [l for l in links if '/squads/' in l] ##filtering through links to only get squads

team_urls = [f"https://fbref.com{l}" for l in links] ## formatting back to links

print(f"Found {len(team_urls)} teams to scrape")
for i, team_url in enumerate(team_urls, 1): 
    team_name = team_url.split("/")[-1].replace("-Stats", "") ##isolating the names of the teams
    print(f"Scraping team {i}/{len(team_urls)}: {team_name}")
    
    try:
        data = requests.get(team_url, headers=headers).text
        soup = BeautifulSoup(data, 'lxml')
        stats = soup.find_all('table', class_ = "stats_table")[0]

        # Convert to DataFrame first
        team_data = pd.read_html(StringIO(str(stats)))[0]
        
        # Handle multi-level columns properly
        if isinstance(team_data.columns, pd.MultiIndex):
            # Flatten multi-level columns by taking the second level (more specific)
            team_data.columns = [col[1] if col[1] != '' else col[0] for col in team_data.columns]
        
        # Select desired columns
        columns_to_keep = ['Player', 'Nation', 'Pos', 'Age', 'MP', 'Starts', 'Min', 'Gls', 'Ast', 'PK', 'CrdY', 'CrdR']
        
        # Check which columns actually exist and keep only those
        available_columns = [col for col in columns_to_keep if col in team_data.columns]
        team_data = team_data[available_columns].copy()
        
        # Add team name
        team_data["Team"] = team_name
        
        # Clean up Age column - extract just the years from "xx-xxx" format
        if 'Age' in team_data.columns:
            team_data['Age'] = team_data['Age'].astype(str).str.split('-').str[0]
            # Convert to numeric, handling any non-numeric values
            team_data['Age'] = pd.to_numeric(team_data['Age'], errors='coerce')
        
        # Remove rows where Player is NaN or contains 'Squad Total' or 'Opponent Total'
        team_data = team_data[team_data['Player'].notna()]
        team_data = team_data[~team_data['Player'].str.contains('Squad Total|Opponent Total', na=False)]
        all_teams.append(team_data) ## appending the data
        
        print(f"Completed {team_name} ({len(team_data)} players).")
    except (requests.RequestException, IndexError, ValueError) as e:
        print(f"Error scraping {team_name}: {e}")
        continue

if all_teams:
    stat_df = pd.concat(all_teams, ignore_index=True) ## concatenating all of the stats
    
    # Clean up the data
    stat_df = stat_df.dropna(subset=['Player'])  # Remove any remaining NaN players
    
    # Remove duplicate columns by keeping only unique column names
    stat_df = stat_df.loc[:, ~stat_df.columns.duplicated()]
    
    # Reorder columns to match database schema
    final_columns = ['Player', 'Nation', 'Pos', 'Age', 'MP', 'Starts', 'Min', 'Gls', 'Ast', 'PK', 'CrdY', 'CrdR', 'Team']
    available_final_columns = [col for col in final_columns if col in stat_df.columns]
    stat_df = stat_df[available_final_columns]
    
    stat_df.to_csv("sp-stats-clean.csv", index=False) ## save without row indices
    print(f"\nSuccessfully scraped {len(all_teams)} teams and saved to 'sp-stats-clean.csv'")
    print(f"Total players: {len(stat_df)}")
else:
    print("No data was successfully scraped")
