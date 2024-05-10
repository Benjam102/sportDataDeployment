import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv
from datetime import datetime

from fora.models import threads, tchat_match_category
from website.models import up_match
from website.scraping.meteo import get_weather, associate_weather_code

# Compétitions d'intérêt
competitions_nom = ["Six Nations", "Premiership", "U20s Six Nations", "Europe Championship", "Top 14", "ProD2", "United Rugby Championship",
                    "Champions Cup", "Challenge Cup", "U20 Championship", "Rugby World Cup", "The Rugby Championship", "Summer Tour", "Autumn Tour"]

# Expressions régulières permettant de retrouver les compétitions malgré des différences de titre dans les articles
competitions = [re.compile(r"^(?!.*(?:Women|U20)).*Six Nations(?!.*women).*", re.IGNORECASE), 
                re.compile(r"^(?!.*Women).*(?!.*Women).*Premiership.*(?!.*Women).*", re.IGNORECASE),
                re.compile(r"^(?!.*Women).*?(U20.*?(?!.*Women)Six Nations|Six Nations(?!.*Women).*?u20).*?(?!.*Women).*", re.IGNORECASE),
                re.compile(r"^(?!.*Women).*Europe.*(?!.*Women).*Championship.*(?!.*Women).*", re.IGNORECASE), 
                re.compile(r".*Top.*14.*", re.IGNORECASE), 
                re.compile(r".*Pro.*D2.*", re.IGNORECASE),
                re.compile(r"^(?!.*Women).*United Rugby Championship.*(?!.*Women).*", re.IGNORECASE), 
                re.compile(r"^(?!.*Women).*Champions.*Cup.*(?!.*Women).*", re.IGNORECASE),
                re.compile(r"^(?!.*Women).*Challenge.*Cup.*(?!.*Women).*", re.IGNORECASE),
                re.compile(r"^(?!.*Women).*?(World.*(?!.*Women).*U20.*?(?!.*Women).*Championship.*(?!.*Women).*|(?!.*Women).*U20.*?Rugby World Cup.*(?!.*Women).*).*(?!.*Women).*", re.IGNORECASE),
                re.compile(r"^(?!.*(?:Women|U20)).*Rugby World Cup.*(?!.*(?:Women|U20)).*", re.IGNORECASE), 
                re.compile(r".*The.*(?!.*Women).*Rugby.*Championship.*(?!.*Women).*", re.IGNORECASE),
                re.compile(r"^(?!.*Women|U20).*Summer(?!.*U20).*", re.IGNORECASE), 
                re.compile(r"^(?!.*Women|U20).*Autumn(?!.*U20).*", re.IGNORECASE)]

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Fonction permettant de récupérer la page html via l'url du site
def get_soup(url: str) -> BeautifulSoup:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def trigger_load_more(url) :
    soup = get_soup(url)
    
    # Searching for a div with attributes : onclick and a specific class
    onclick = soup.find('div', {'onclick': 'FixturesResultsView.loadMore();', 'class': 'load-more'})

    print(onclick)
    
    # Check if the onclick exists
    if onclick :
                                                                       # Create options for Chrome browser
        options = Options()
        options.add_argument('--headless')                              # Run the browser in headless mode (without graphical interface)
        options.add_argument('--disable-gpu')                           # Disable GPU rendering
        options.add_argument('--log-level=3')                           # Disable Chrome logging messages
        
        # Simulate the event using Selenium
        driver = webdriver.Chrome(options=options)                      # Initialize the webdriver 
        driver.get(url)                                                 # Open the page in the browser
        driver.execute_script(onclick['onclick'])                       # Trigger the onclick event

        # Wait for a certain amount of time for the content to load
        time.sleep(0.15)                                                

        new_soup = BeautifulSoup(driver.page_source, 'html.parser')     # Get the updated page source
        driver.quit()                                                   # Close the browser
        return new_soup

def date(soup_game_date: list) :
    month = months.index(soup_game_date[1]) + 1
    day = soup_game_date[2][:-1]
    if month < 10 : 
        month = "0" + str(month)
    
    if int(day) < 10 :
        day = "0" + day

    whole_date = soup_game_date[3] + "-"+ str(month) +  "-" + day # Suppression de la virgule pour le jour 

    return whole_date

def get_upcoming_matches(url: str) -> BeautifulSoup :
    # Extend the page
    soup = trigger_load_more(url)
        
    #soup = get_soup(url)
    soup_game = soup.find_all('div', class_='games-list-item')
    print(len(soup_game))

    for k in range(len(soup_game)) :
        soup_game_date = soup_game[k].find(class_='date').get_text().split()
        whole_date = date(soup_game_date)                                                                 # A retenir : date
        #print(whole_date)

        # Balise comp contenant les différentes informations (équipes, heure, stade...)
        b_comp = soup_game[k].find_all(class_='comp')

        for comp in b_comp :
            # Balise h2 qui contient la compétition
            competition_name = comp.find("h2").get_text()
            #print(competition_name)

            for index, t in enumerate(competitions) :
                
                if re.match(t, competition_name) :
                    name_competition = competitions_nom[index]                                             # A retenir : nom competition
                
                    games_day = comp.find(class_='games')
                    match_day = games_day.find_all(class_='game')

                    for match in match_day :
                        time_ = match.find(class_="time").find(class_="state").get_text().split()[0]      # A retenir : nom competition
                        hour_24 = datetime.strptime(time_, "%I:%M%p").strftime("%H:%M")
                        #print(time_)
                        stadium = match.find(class_="time").find(class_="venue").get_text().strip()       # A retenir : nom competition
                        #print(stadium)
                        team_home1 = match.find(class_="team home").get_text().strip()                  # A retenir : nom competition
                        #print(team_home)
                        logo_team_home1 = match.find(class_="team home").find("span").find("img").get("data-src") # A retenir : nom competition
                        #print(logo_team_home)
                        team_away2 = match.find(class_="team away").get_text().strip()
                        #print(team_away2)
                        logo_team_away = match.find(class_="team away").find("span").find("img").get("data-src")
                        #print(logo_team_away)
                        score = "-"
                        #print(score)
                        round_ = match.find(class_="round").get_text()
                        #print(round_)
                        
                        find_match = up_match.objects.filter(team_home = team_home1, team_away = team_away2, league = name_competition, date = whole_date)
                        #print(find_match)
                        if not find_match.exists(): 
                            
                            weather = get_weather(stadium, whole_date, int(hour_24[:2]))     # On met que les heures
                            
                            if weather != None :
                                path_code = associate_weather_code(weather['weather_code'])
                                temperature_ = float(weather['temperature_2m'])
                                humidity_ = float(weather['relative_humidity_2m'])
                                pressure_ = float(weather['surface_pressure'])
                                precipitation_ = float(weather['precipitation'])
                                wind_speed_ = float(weather['wind_speed_10m'])
                                code_ = float(weather['weather_code'])
                            else :
                                path_code = None
                                temperature_ = None
                                humidity_ = None
                                pressure_ = None
                                precipitation_ = None
                                wind_speed_ = None
                                code_ = None
                                
                            new_match = up_match(
                                status = 'Scheduled',
                                team_home = team_home1,
                                team_away = team_away2,
                                score_home = None,
                                score_away = None,
                                referee = None,
                                date = whole_date,
                                hour = hour_24,
                                stade_name = stadium,
                                league = name_competition,
                                phase = round_,
                                temperature = temperature_,
                                humidity = humidity_,
                                pressure = pressure_,
                                precipitation = precipitation_,
                                wind_speed = wind_speed_,
                                code = code_,
                                code_url = path_code,
                                neutrality = None
                            )
                            
                            new_match.save()
                            
                            # Créer un nouveau thread associé au match
                            cate_match = tchat_match_category.objects.get(title=new_match.league)
                            new_thread = threads.objects.create(match=new_match, category=cate_match)

                            new_thread.save()

                        