import re

chemin_img = ["/IMG/meteo/soleil_0.png",
              "/IMG/meteo/nusoleil_1_2_3.png",
              "/IMG/meteo/brouillard_45_48.png",
              "/IMG/meteo/bruine_51_53_55.png",
              "/IMG/meteo/pluie_56_57_61_63_65_66_67.png",
              "/IMG/meteo/neigeux_71_73_75.png",
              "/IMG/meteo/neigeux_77.png",
              "/IMG/meteo/pluvieux_80_81_82.png",
              "/IMG/meteo/neigeux_85_86.png",
              "/IMG/meteo/orage_95.png",
              "/IMG/meteo/orage_96_99.png"
              ]


def associate_weather_code(code) :
    """
    Function that associate an image with the code given by the open-meteo API for the general weather.

    Parameters:
        code: Int that indicate the general weather.

    Returns:
        form_home_team_match: String corresponding to the path of the image representing the general weather. 
                              None else.  
    """
    if code != None :
        for index, c in enumerate(chemin_img) :
            # Use a regular expression to extract all the numbers in the path in the form of an array 
            nombres = re.findall(r'\d+', c) # (\d = [0, 9]) and + to have several figures
            
            if str(code) in nombres :
                return chemin_img[index]

    return None


def form_match(matches_team, team) :
    """
    Function that combines the results of the 5 most recent matches for a team passed in parameter in relation to the current
    match in the view.

    Parameters:
        matches_team: Queryset which contains the 5 most recent matches of the team passed in parameter.
        team: Team of interest.

    Returns:
        form_home_team_match: List of tuples. We associate a match with his result (V: victory, N: draw, D: defeat).
    """
    form_home_team_match = []

    if (team != None) :
        for m in matches_team :
            # Home team
            if m.home_team.name == team :    
                if m.home_score > m.away_score :
                    result = 'V'
                elif m.home_score == m.away_score :
                    result = 'N'
                else :
                    result = 'D'
            # Away team
            else :                                         
                if m.home_score > m.away_score :
                    result = 'D'
                elif m.home_score == m.away_score :
                    result = 'N'
                else :
                    result = 'V'

            form_home_team_match.append((result, m))
    
    return form_home_team_match


def integer_prediction(nb) :
    """
    Function that allows us to avoid having 10.0. We want to remove the 0. 

    Parameters:
        nb: Number to modify id it's necessary.

    Returns:
        nb: The number modify or not.
    """

    if nb == int(nb):
        return int(nb)
    else:
        return nb
    

def user_prediction(prediction) :
    """
    Function that allow us to calculate the user predictions. 

    Parameters:
        prediction: model that contains the user prediction.

    Returns:
        home_prediction1: early prediction for home team if any otherwise none.
        away_prediction1: early prediction for away team if any otherwise none.
        home_prediction2: final prediction for home team if any otherwise none.
        away_prediction2: final prediction for away team if any otherwise none.
    """
    
    if prediction.prediction_margin1 != None and prediction.prediction_margin2 != None :
        home_prediction1 = integer_prediction((prediction.prediction_margin1 + prediction.prediction_total1)/2)
        away_prediction1 = integer_prediction(prediction.prediction_total1 - home_prediction1)

        home_prediction2 = integer_prediction((prediction.prediction_margin2 + prediction.prediction_total2)/2)
        away_prediction2 = integer_prediction(prediction.prediction_total2 - home_prediction2)
    
    elif prediction.prediction_margin1 != None and prediction.prediction_margin2 == None :
        home_prediction1 = integer_prediction((prediction.prediction_margin1 + prediction.prediction_total1)/2)
        away_prediction1 = integer_prediction(prediction.prediction_total1 - home_prediction1)
        
        home_prediction2 = None
        away_prediction2 = None
    
    elif prediction.prediction_margin1 == None and prediction.prediction_margin2 != None :
        home_prediction1 = None
        away_prediction1 = None
        
        home_prediction2 = integer_prediction((prediction.prediction_margin2 + prediction.prediction_total2)/2)
        away_prediction2 = integer_prediction(prediction.prediction_total2 - home_prediction2)

    return home_prediction1, away_prediction1, home_prediction2, away_prediction2


