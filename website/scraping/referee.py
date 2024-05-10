import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

# Importation de la table match
from website.models import up_match
from fuzzywuzzy import fuzz

# Nombre d'articles sur la première page à scrappper(Max : 10)
NB_ARTICLES = 1

# Compétitions d'intérêt
competitions_nom = ["Six Nation", "Premiership", "U20s Six Nation", "Europe Championship", "Top 14", "ProD2", "United Rugby Championship",
                    "Champions Cup", "Challenge Cup", "U20 Championship", "Rugby World Cup", "The Rugby Championship", "Summer Tour", "Autumn Tour"]

# Expressions régulières permettant de retrouver les compétitions malgré des différences de titre dans les articles
competitions = [r"^(?!.*(?:Women|U20)).*Six Nations(?!.*women).*", r"^(?!.*Women).*England:.*(?!.*Women).*Premiership.*(?!.*Women).*",
                r"^(?!.*Women).*?(U20.*?(?!.*Women)Six Nations|Six Nations(?!.*Women).*?u20).*?(?!.*Women).*",
                r"^(?!.*Women).*Europe.*(?!.*Women).*Championship.*(?!.*Women).*", r".*Top.*14.*", r".*Pro.*D2.*",
                r"^(?!.*Women).*United Rugby Championship.*(?!.*Women).*", r"^(?!.*Women).*Champions.*Cup.*(?!.*Women).*",
                r"^(?!.*Women).*Challenge.*Cup.*(?!.*Women).*",
                r"^(?!.*Women).*?(World.*(?!.*Women).*U20.*?(?!.*Women).*Championship.*(?!.*Women).*|(?!.*Women).*U20.*?Rugby World Cup.*(?!.*Women).*).*(?!.*Women).*",
                r"^(?!.*(?:Women|U20)).*Rugby World Cup.*(?!.*(?:Women|U20)).*", r".*The.*(?!.*Women).*Rugby.*Championship.*(?!.*Women).*",
                r"^(?!.*Women|U20).*Summer(?!.*U20).*", r"^(?!.*Women|U20).*Autumn(?!.*U20).*"]

# Fonction permettant de récupérer la page html via l'url du site
def get_soup(url: str) -> BeautifulSoup:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Fonction permettant de récupérer les arbitres pour les matchs à venir
def get_referee(url: str) -> BeautifulSoup:
    soup = get_soup(url)
    soup_header = soup.find_all(class_='entry-title mh-posts-list-title')
    
    # Récupération des liens vers les articles présents dans les classes 'entry-title mh-posts-list-title'
    url_articles = []
    for k in range(NB_ARTICLES) :
        b_a = soup_header[k].find('a')                    # On récupère les balises a 
        b_href = b_a.get('href')
        url_articles.append(b_href)                       # On récupère les liens des articles

    # Scrapping des différents articles
    for url in url_articles :
        soup_article = get_soup(url)
        
        for index, comp in enumerate(competitions) :
            exp_reg_comp = re.compile(comp, re.IGNORECASE)

            # Récupération de la balise h2 correspondante à la compétition si elle existe à partir de son nom en expression régulière
            soup_article_h2 = soup_article.find_all(class_='wp-block-heading', string=exp_reg_comp)
            
            # Possibilité d'avoir plusieurs balises h2 pour le même titre
            for k in range(len(soup_article_h2)) :

                if soup_article_h2[k] :
                    # Récupération des balises suivantes (notamment les balises p car elles contiennent les arbitres des matchs à venir)
                    balises_suivante = soup_article_h2[k].find_next_siblings()

                    for p in balises_suivante :
                        # On laisse passer les balises h3 car ils contiennent des informations pour d'autres matchs de la même ligue
                        if p.name == "p" or p.name == "h3" :
                            # Si on a bien une balise p
                            if p.name == "p" :
                                p_soup = p.find_all("strong")                               # Contient normalement le match ("Team1 v Team2") mais aussi 
                                                                                            # d'autres choses des fois en plus
                                for j in range(len(p_soup)) :

                                    # Pas de match si la balise strong est nulle
                                    if p_soup[j] != None :
                                        match = p_soup[j].get_text()
                                        equipes = match.split(" v ")                        # Récupération des deux équipes

                                        if (len(equipes) > 1) :                             # Si la balise strong contient un match
                                            equipe_1_propre = equipes[0].split(": ")        # Cas où on aurait quelque chose avant la 1ère équipe
                                            equipe_2_propre = equipes[1].split(" – ")       # Cas où on aurait quelque chose après la 2ème équipe

                                            if (len(equipe_1_propre) > 1) :
                                                # Des fois, on peut avoir "final: France" 
                                                team_h = equipe_1_propre[1]
                                            else :
                                                team_h = equipe_1_propre[0]
                                            
                                            if (len(equipe_2_propre) > 1) :
                                                # Des fois, on peut avoir des pools
                                                team_a = equipe_2_propre[0]
                                                # pool = equipe_2_propre[1] -> si on souhaite récupérer les pools
                                            else :
                                                team_a = equipe_2_propre[0]
                                        
                                            # Recherche de la sous-chaine commençant par Referee
                                            ligne_arbitre = p.find(string=lambda text : 'Referee' in text)
                            
                                            # Recherche du nom et prénom
                                            nom_arbitre_match = re.search(r'Referee:(?:&nbsp;)?\s*([^<(]+)', ligne_arbitre)
                            
                                            if nom_arbitre_match :
                                                arbitre = nom_arbitre_match.group(1)
                                            else :
                                                # Changement d'arbitre
                                                ancien_arbitre = p.find_next("s")         # pour trouver la balise s suivant la p actuelle
                                                nouvel_arbitre = ancien_arbitre.find_next_sibling(string=True)

                                                # strip() -> enlève espace début/fin, rsplit(séparateur, cb de séparation) -> 0 nom/prénom et 1 nationalité car D -> G
                                                arbitre = nouvel_arbitre.strip().rsplit(' ', 1)[0]
                                                
                                            compet = competitions_nom[index]
                                            
                                            # BDD
                                            find_match = up_match.objects.filter(league = compet, referee = None)
                                            #print("\n", find_match, "\n")

                                            for m in find_match :

                                                # Comparaison floue des noms des équipes
                                                team_home_ratio = fuzz.ratio(m.team_home.lower(), team_h.lower())
                                                team_away_ratio = fuzz.ratio(m.team_away.lower(), team_a.lower())
    
                                                # Si les ratios sont élevés (signifiant une correspondance raisonnable)
                                                if team_home_ratio > 75 and team_away_ratio > 75:
                                                    m.referee = arbitre
                                                    m.save()            
                                                                    

                            # cas ou on a des balises h3 qui ne nous intéressent pas
                            else : 
                                continue
                        else :
                            break
        #break # une url pour l'instant  
        