##importing all required libraries
from bs4 import BeautifulSoup
import pandas as pd
import requests 
import time
from io import StringIO

all_teams = [] ## list to store all teams

try:
    html = requests.get('https://fbref.com/en/comps/40/Scottish-Premiership-Stats').text ##getting the html from the website
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table', class_ = 'stats_table')[0] ##only want the first table, therefore the first index
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
        data = requests.get(team_url).text
        soup = BeautifulSoup(data, 'lxml')
        stats = soup.find_all('table', class_ = "stats_table")[0]

        if stats and stats.columns: stats.columns = stats.columns.droplevel() ##formatting the stats

        # Assuming 'team_data' is a BeautifulSoup Tag
        # Convert it into a DataFrame
        team_data = pd.read_html(StringIO(str(stats)))[0]
        team_data["Team"]= team_name
        all_teams.append(team_data) ## appending the data
        
        print(f"✓ Completed {team_name}. Waiting 5 seconds...")
    except (requests.RequestException, IndexError, ValueError) as e:
        print(f"✗ Error scraping {team_name}: {e}")
        continue
    
    time.sleep(5) ## making sure we don't get blocked from scraping by delaying each loop by 5 seconds

if all_teams:
    stat_df = pd.concat(all_teams) ## concatenating all of the stats
    stat_df.to_csv("sp-stats.csv") ## importing to csv
    print(f"\n Successfully scraped {len(all_teams)} teams and saved")
    print(f"Total rows: {len(stat_df)}")
else:
    print("No data was successfully scraped")
