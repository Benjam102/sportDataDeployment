from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from datetime import datetime, timedelta
from fora.utils import sort_key
from django.http import JsonResponse

# Models
from website.models import matches
from fora.models import tchats, tchat_posts, threads_categories_match, threads_comments_match, threads_match

def fora(request) :
    """
    View function to render the main forum page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered forum page.
    """

    ''' Part: Categories and leagues '''
    # Retrieve all unique categories (club, international, other)
    categories = threads_categories_match.objects.values_list('thread_category', flat=True).order_by('thread_category').distinct()

    leagues_by_categories = {}

    # Associate each league with its respective category
    for category in categories:
        leagues = threads_categories_match.objects.filter(thread_category=category).order_by('thread_league')
        leagues_by_categories[category] = leagues

    ''' Part: Tchats '''
    tchats_ = tchats.objects.all().order_by('tchat_category')

    tchats_by_categories = {}

    # Associate each tchat with its respective category
    for tchat in tchats_:
        tchats_by_categories[tchat.tchat_category] = []

    for tchat in tchats_:
        # Create a dictionary containing information about the current tchat
        tchat_info = {
            'tchat_category': tchat.tchat_category,
            'tchat_name': tchat.tchat_name,
            'tchat_slug': tchat.slug_tchat_name,
        }
 
        tchats_by_categories[tchat.tchat_category].append(tchat_info)

    # Create a context dictionary containing categories and tchats_info
    context = {
        'leagues_by_categories': leagues_by_categories,
        'tchats_by_categories': tchats_by_categories,
    }

    # Render the fora.html template with the context data
    return render(request, "fora.html", context)

def categories(request, slug_thread_category, slug_thread_league) :
    category_selected = threads_categories_match.objects.get(slug_thread_league=slug_thread_league)
    id_category_selected = threads_categories_match.objects.get(slug_thread_league=slug_thread_league)     # sans rien preciser on recupere l id autogenere

    corresponding_threads = threads_match.objects.filter(category=id_category_selected)

    threads_info = []
    for thread in corresponding_threads :

        # Récupérer la date du commentaire le plus récent pour ce thread
        thread_comments = threads_comments_match.objects.filter(thread=thread)
        latest_comment = thread_comments.aggregate(latest_comment=Max('date'))['latest_comment'] #car dictionnaire
        
        # Compter le nombre total de commentaires pour ce thread
        comments_count = threads_comments_match.objects.filter(thread=thread).count()

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

def threads_(request, slug_thread_category, slug_thread_league, slug_thread_comments) :
    """
    View function to render the thread of the discussion.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_thread_category: Part of the url that indicates the category (club, international or other).
        slug_thread_league: Part of the url that indicates the league (challenge cup, top 14, proD2...).
        slug_thread_comments: Part of the url that indicates the current thread.

    Returns:
        HttpResponse: The HTTP response containing the rendered thread page.
    """
    match_ = matches.objects.get(key_id=slug_thread_comments)
    thread_exist = True

    try :
        thread_ = threads_match.objects.get(match=match_)
        comments = threads_comments_match.objects.filter(thread=thread_).order_by('date')
    except threads_match.DoesNotExist : # Pour les anciens matches
        thread_ = None
        comments = None
        thread_exist = False

    # For the tchat -> allow us to have Today, yesterday
    today_date = datetime.now().date()
    yesterday_date = today_date - timedelta(days=1)

    context = {
        'comments': comments,
        'today_date': today_date,
        'yesterday_date': yesterday_date,
        'slug_category': slug_thread_league,
        'slug_thread': slug_thread_comments,
        'thread_exist': thread_exist,
    }

    return render(request, "thread.html", context)

def tchats_(request, slug_tchat_category, slug_tchat_name) :
    tchat_ = tchats.objects.get(slug_tchat_name=slug_tchat_name)
    comments = tchat_posts.objects.filter(tchat=tchat_).order_by('date')

    # For the tchat -> allow us to have Today, yesterday
    today_date = datetime.now().date()
    yesterday_date = today_date - timedelta(days=1)

    context = {
        "comments": comments,
        "today_date": today_date,
        "yesterday_date": yesterday_date,
        "slug_tchat_category": slug_tchat_category,
        "slug_tchat_name": slug_tchat_name,
    }

    return render(request, "tchat.html", context)

def add_comment_thread(request, slug_comment_category, slug_thread_tchat):
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user

        if content :
            match_id = get_object_or_404(matches, key_id=slug_thread_tchat)
            thread_id = threads_match.objects.get(match=match_id)
            new_comment = threads_comments_match.objects.create(user=user, thread=thread_id, content=content)

            # Prepare data to send back as JSON response
            comment_data = {
                'username': user.username,
                'date': new_comment.date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
                'content': new_comment.content
            }
            return JsonResponse(comment_data)  # Return the new comment data as JSON response

def add_comment_tchat(request, slug_tchat_name) :
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user

    if content :
        tchat_id = get_object_or_404(tchats, slug_tchat_name= slug_tchat_name)
        new_comment = tchat_posts.objects.create(user=user, tchat=tchat_id, content=content)

        # Prepare data to send back as JSON response
        comment_data = {
            'username': user.username,
            'date': new_comment.date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
            'content': new_comment.content
        }
        
        return JsonResponse(comment_data)  # Return the new comment data as JSON response

def display_threads(request, slug_category_thread) :
    category_selected = threads_categories_match.objects.get(slug_thread_league=slug_category_thread)     # sans rien preciser on recupere l id autogenere
    
    corresponding_threads = threads_match.objects.filter(category=category_selected, closed=False)

    threads_info = []
    for thread in corresponding_threads :

        # Récupérer la date du commentaire le plus récent pour ce thread
        thread_comments = threads_comments_match.objects.filter(thread=thread)
        latest_comment = thread_comments.aggregate(latest_comment=Max('date'))['latest_comment'] #car dictionnaire
        
        # Compter le nombre total de commentaires pour ce thread
        comments_count = threads_comments_match.objects.filter(thread=thread).count()

        thread_info = {
                'slug_thread': thread.match.key_id,
                'latest_comment': str(latest_comment),
                'comments_count': comments_count,
                'closed_thread': thread.closed,
                'category_selected': category_selected.slug_thread_league,
                'slug_country': category_selected.slug_thread_category,
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
            'no_data': "No threads selected",
        }
    
    return JsonResponse(context)  # convertir les donnees pythons pour que js les comprenne

def display_tchats(request, slug_tchat_name) :
    tchat_selected = tchats.objects.get(slug_tchat_name=slug_tchat_name)

    corresponding_posts = tchat_posts.objects.filter(tchat=tchat_selected)

    # Get the date of the latest post for the current tchat
    latest_post_date = corresponding_posts.aggregate(latest_post_date=Max('date'))['latest_post_date'] # dictionary
    
    # Retrieve the latest post
    if latest_post_date is not None:
        latest_post = tchat_posts.objects.get(tchat=tchat_selected, date=latest_post_date)
    else:
        latest_post = None 

    # Count the total number of posts for the current tchat
    post_count = tchat_posts.objects.filter(tchat=tchat_selected).count()
          
    # Create a dictionary containing information about the current tchat
    context = {
        'post_count': int(post_count),
        'latest_post_date': str(latest_post_date),
        'latest_post': str(latest_post),
        'tchat_slug_category': tchat_selected.slug_tchat_category,
        'tchat_slug_name': tchat_selected.slug_tchat_name,
    }
    
    return JsonResponse(context)
 
    

