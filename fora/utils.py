import datetime

def sort_key(dico):
    """
    Function to sort comments by date. It transforms strings into datetime if a date is present.

    Parameters:
        dico: python dictionary containing information about a comment, including the date.

    Returns:
        dateTime object
    """
    if dico['latest_comment'] == 'None':
        # Set time zone to minus infinity if no comment is found (element == None)
        return datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)            
    else:
        return datetime.datetime.fromisoformat(dico['latest_comment'])