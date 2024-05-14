from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from datetime import datetime, timedelta
from fora.utils import sort_key
from django.http import JsonResponse

# Models
from website.models import up_match
from fora.models import tchat_match_category, tchat_match_comment, threads

def fora(request) :
    # Récupérer tous les noms des catégories sans doublon, triés par ordre alphabétique
    categories = tchat_match_category.objects.values_list('country', flat=True).order_by('country').distinct()

    # Créer un dictionnaire pour stocker les leagues par catégories
    leagues_by_categories = {}

    # Lier chaque league à une catégorie
    for category in categories:
        categories = tchat_match_category.objects.filter(country=category).order_by('title')
        leagues_by_categories[category] = categories
    
    context = {
        'categories_by_country': leagues_by_categories,
    }

    return render(request, "fora.html", context)

def categories(request, slug_type, slug_category) :
    category_selected = tchat_match_category.objects.get(slug_title=slug_category)
    id_category_selected = tchat_match_category.objects.get(slug_title=slug_category)     # sans rien preciser on recupere l id autogenere

    corresponding_threads = threads.objects.filter(category=id_category_selected)

    threads_info = []
    for thread in corresponding_threads :

        # Récupérer la date du commentaire le plus récent pour ce thread
        thread_comments = tchat_match_comment.objects.filter(thread=thread)
        latest_comment = thread_comments.aggregate(latest_comment=Max('date'))['latest_comment'] #car dictionnaire
        
        # Compter le nombre total de commentaires pour ce thread
        comments_count = tchat_match_comment.objects.filter(thread=thread).count()

        thread_info = {
            'slug_thread': thread.match.slug,
            'latest_comment': latest_comment,
            'comments_count': comments_count,
            'closed_thread': thread.closed,
            }

        # Ajouter le dictionnaire à la liste
        threads_info.append(thread_info)
    
    # Trier la liste par date du commentaire le plus récent
    sorted_threads_info = sorted(threads_info, key=sort_key, reverse=True)

    today_date = datetime.now().date()

    context = {
        'category_selected': category_selected,
        'sorted_threads_info': sorted_threads_info,
        'l_corresponding_threads': len(corresponding_threads),
        'today_date': str(today_date),
    }

    return render(request, "category.html", context)

def threads_(request, slug_type, slug_category, slug_thread) :
    match_ = up_match.objects.get(slug=slug_thread)
    thread_ = threads.objects.get(match=match_)
    comments = tchat_match_comment.objects.filter(thread=thread_).order_by('date')

    # For the tchat -> allow us to have Today, yesterday
    today_date = datetime.now().date()
    yesterday_date = today_date - timedelta(days=1)

    context = {
        "comments": comments,
        "today_date": today_date,
        "yesterday_date": yesterday_date,
        "slug_category": slug_category,
        "slug_thread": slug_thread,
    }

    return render(request, "thread.html", context)

def add_comment(request, slug_category, slug_thread):
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user

        if content :
            match_id = get_object_or_404(up_match, slug=slug_thread)
            thread_id = threads.objects.get(match=match_id)
            new_comment = tchat_match_comment.objects.create(user=user, thread=thread_id, content=content)

            # Prepare data to send back as JSON response
            comment_data = {
                'username': user.username,
                'date': new_comment.date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
                'content': new_comment.content
            }
            return JsonResponse(comment_data)  # Return the new comment data as JSON response
        
def display_category(request, slug_category) :
    category_selected = tchat_match_category.objects.get(slug_title=slug_category)     # sans rien preciser on recupere l id autogenere
    
    corresponding_threads = threads.objects.filter(category=category_selected, closed=False)

    threads_info = []
    for thread in corresponding_threads :

        # Récupérer la date du commentaire le plus récent pour ce thread
        thread_comments = tchat_match_comment.objects.filter(thread=thread)
        latest_comment = thread_comments.aggregate(latest_comment=Max('date'))['latest_comment'] #car dictionnaire
        
        # Compter le nombre total de commentaires pour ce thread
        comments_count = tchat_match_comment.objects.filter(thread=thread).count()

        thread_info = {
                'slug_thread': thread.match.slug,
                'latest_comment': str(latest_comment),
                'comments_count': comments_count,
                'closed_thread': thread.closed,
                'category_selected': category_selected.slug_title,
                'slug_country': category_selected.slug_country,
            }

        # Ajouter le dictionnaire à la liste
        threads_info.append(thread_info)
    
    if len(threads_info) > 0 :
        # Trier la liste par date du commentaire le plus récent
        sorted_threads_info = sorted(threads_info, key=sort_key, reverse=True)

        today_date = datetime.now().date()

        context = {
            
            'sorted_threads_info': sorted_threads_info,
            'today_date': today_date,
        }

    else :
        context = {
            'no_data': "No threads",
        }
    
    return JsonResponse(context)  # convertir les donnees pythons pour que js les comprenne