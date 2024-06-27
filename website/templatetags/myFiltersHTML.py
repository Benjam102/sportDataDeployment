from django import template

register = template.Library()

@register.filter
def cut_before_first_space(value):
    try:
        last_name1 = value.split(' ', 1)[1]
        last_name2 = last_name1.split('(', 1)[0] # des fois y a des trucs entre apranthese
        return  last_name2 # Divise la chaîne en deux parties sur le premier espace et retourne la deuxième partie
    except Exception:
        return value                   # Si la chaîne est vide ou ne contient pas d'espace, retourne une chaîne vide

@register.filter
def split(value, delimiter=' '):
    return value.split(delimiter)

