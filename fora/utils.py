import datetime

def sort_key(dico):
    if dico['latest_comment'] is None:
        # Mettre les éléments avec None en bas de la liste (-infini) et on met un fuseau horaire
        return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)            
    else:
        return dico['latest_comment']