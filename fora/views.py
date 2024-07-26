from django.shortcuts import render
from django.db.models import Max
from datetime import datetime, timedelta
from django.http import JsonResponse

# Useful function
from fora.utils import sort_key

# Model import
from website.models import matches
from fora.models import tchats, tchat_posts, threads_categories_match, threads_comments_match, threads_match
from accounts.models import favourites

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
    categories = threads_categories_match.objects.values_list('thread_category', flat=True).distinct()

    leagues_by_categories = {}

    # Associate each league with its respective category
    for category in categories:
        leagues = threads_categories_match.objects.filter(thread_category=category).order_by('thread_league')

        if (category != 'Favourites') :
            leagues_by_categories[category] = leagues
        else :
            leagues_by_categories[category] = []

    # Favoris
    compe_fav = []
    if request.user.is_authenticated:
        user = request.user
        competitions_favourites = favourites.objects.filter(user=user)

        for c in competitions_favourites :   
            dico = {                                            # mettre les memes nom que pour les objets threads_category
                'slug_thread_league': c.slug_competition,
                'slug_thread_category': threads_categories_match.objects.get(slug_thread_league=c.slug_competition).slug_thread_category,
                'thread_league': c.name_competition
            }
            leagues_by_categories['Favourites'].append(dico)
            compe_fav.append(c.name_competition)

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
        'compe_fav': compe_fav,
    }

    # Render the fora.html template with the context data
    return render(request, "fora.html", context)


def categories(request, slug_thread_category, slug_thread_league) :
    """
    View function to render threads relative to a competition (URC, Top 14...)

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_thread_category: Part of the url that indicates the category (club, international or other).
        slug_thread_league: Part of the url that indicates the league (challenge cup, top 14, proD2...).

    Returns:
        HttpResponse: The HTTP response containing the page with treads for one competition.
    """
    category_selected = threads_categories_match.objects.get(slug_thread_league=slug_thread_league)   
    corresponding_threads = threads_match.objects.filter(category=category_selected)

    threads_info = []
    for thread in corresponding_threads :

        # Retrieve the date of the most recent comment for this thread
        thread_comments = threads_comments_match.objects.filter(thread=thread)
        latest_comment = thread_comments.aggregate(latest_comment=Max('date'))['latest_comment'] #car dictionnaire
        
        # Count the total number of comments for this thread
        comments_count = threads_comments_match.objects.filter(thread=thread).count()

        thread_info = {
            'slug_thread': thread.match.key_id,
            'latest_comment': str(latest_comment),
            'comments_count': comments_count,
            'closed_thread': thread.closed,
            }

        # Add dictionary to list
        threads_info.append(thread_info)
    
    # Sort list by date of most recent comment
    sorted_threads_info = sorted(threads_info, key=sort_key, reverse=True)

    today_date = datetime.now().date()

    print(sorted_threads_info)
    context = {
        'category_selected': category_selected,
        'sorted_threads_info': sorted_threads_info,
        'l_corresponding_threads': len(corresponding_threads),
        'today_date': str(today_date),
    }

    return render(request, "category.html", context)


def threads_(request, slug_thread_category, slug_thread_league, slug_thread_comments) :
    """
    View function to render the discussion of a thread.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_thread_category: Part of the url that indicates the category (club, international or other).
        slug_thread_league: Part of the url that indicates the league (challenge cup, top 14, proD2...).
        slug_thread_comments: Part of the url that indicates the current thread.

    Returns:
        HttpResponse: The HTTP response containing the rendered discussion page for a thread.
    """
    match_ = matches.objects.get(key_id=slug_thread_comments)
    thread_exist = True

    try :
        thread_ = threads_match.objects.get(key_id=match_.key_id)
        comments = threads_comments_match.objects.filter(thread=thread_).order_by('date')

        if(thread_.closed == False) :
            thread_exist = False
            
    # for past matches
    except threads_match.DoesNotExist : 
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
    """
    View function to render the discussion of a tchat.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_thread_category: Part of the url that indicates the category (club, international or other).
        slug_thread_name: Part of the url that indicates the tchat (Irish, French, General).

    Returns:
        HttpResponse: The HTTP response containing the rendered discussion page for a tchat.
    """
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
    """
    View function to add a comment in a discussion of a thread.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_thread_category: Part of the url that indicates the competition (Top 14, Pro D2...).
        slug_thread_tchat: Part of the url that indicates the match relative to a thread.

    Returns:
        JsonResponse: 1. If the request method is 'POST' and the comment is successfully added to the discussion,
                         it returns a JSON response with details of the added comment.
                      2. If the request method is not 'POST', it returns a JSON response which is equal to none.
    """
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user

        if content :
            thread_id = threads_match.objects.get(key_id=slug_thread_tchat)
            new_comment = threads_comments_match.objects.create(user=user, thread=thread_id, content=content)

            # Prepare data to send back as JSON response
            comment_data = {
                'username': user.username,
                'date': new_comment.date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
                'content': new_comment.content
            }

            # Return the new comment data as JSON response
            return JsonResponse(comment_data)  
        
    else :
        context = None
        return JsonResponse(context)


def add_comment_tchat(request, slug_tchat_name) :
    """
    View function to add a comment in a discussion of a tchat.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_tchat_name: Part of the url that indicates the tchat where we want to add a comment.

    Returns:
        JsonResponse: 1. If the request method is 'POST' and the comment is successfully added to the tchat,
                         it returns a JSON response with details of the added comment.
                      2. If the request method is not 'POST', it returns a JSON response which is equal to none.
    """
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user

    if content :
        tchat_id = tchats.objects.get(slug_tchat_name= slug_tchat_name) 
        new_comment = tchat_posts.objects.create(user=user, tchat=tchat_id, content=content)

        # Prepare data to send back as JSON response
        comment_data = {
            'username': user.username,
            'date': new_comment.date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
            'content': new_comment.content
        }
        
        # Return the new comment data as JSON response
        return JsonResponse(comment_data)  

    else :
        context = None
        return JsonResponse(context)


def display_threads(request, slug_category_thread) :
    """
    View function to display threads based on the competition selected.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_thread_league: Part of the url that indicates the competition selected (challenge cup, top 14...).

    Returns:
        JsonResponse: 1. If the request method is 'GET', it returns a JSON response with details of sorted threads corresponding
                         to the competition selected.
                      2. If the request method is not 'GET', it returns a JSON response which is equal to none.
    """
    if request.method == 'GET':
        category_selected = threads_categories_match.objects.get(slug_thread_league=slug_category_thread)  
     
        if(category_selected.thread_league != 'Closest') :
            corresponding_threads = threads_match.objects.filter(category=category_selected, closed=False)
        else :
            # if recent is selected, no particular category is chosen
            corresponding_threads = threads_match.objects.filter(closed=False)

        threads_info = []
        for thread in corresponding_threads :

            # Retrieve the date of the most recent comment for this thread
            thread_comments = threads_comments_match.objects.filter(thread=thread)
            latest_comment = thread_comments.aggregate(latest_comment=Max('date'))['latest_comment'] #car dictionnaire
         
            # Count the total number of comments for this thread
            comments_count = threads_comments_match.objects.filter(thread=thread).count()

            thread_info = {
                    'slug_thread': thread.key_id,
                    'latest_comment': str(latest_comment),
                    'comments_count': comments_count,
                    'closed_thread': thread.closed,
                    'category_selected': category_selected.slug_thread_league,
                    'slug_country': category_selected.slug_thread_category,
                }
            
            # Add dictionary to list
            threads_info.append(thread_info)
            
        if len(threads_info) > 0 :
            # Sort list by date of most recent comment
            sorted_threads_info = sorted(threads_info, key=sort_key, reverse=True)

            today_date = datetime.now().date()
            yesterday_date = today_date - timedelta(days=1)

            if (category_selected == 'Closest') :
                # Display only the first 10
                sorted_threads_info = sorted_threads_info[:10]
            
            context = {
                
                'sorted_threads_info': sorted_threads_info,
                'today_date': today_date,
                'yesterday_date': yesterday_date,
            }

        else :
            context = {
                'no_data': "No threads selected",
            }
        
        return JsonResponse(context)
    
    else :
        context = None
        return JsonResponse(context)
    

def display_tchats(request, slug_tchat_name) :
    """
    View function to display the tchat selected.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_thread_name: Part of the url that indicates the tchat selected (French, Iris, General).

    Returns:
        JsonResponse: 1. If the request method is 'GET', it returns a JSON response with details on the tchat selected.
                      2. If the request method is not 'GET', it returns a JSON response which is equal to none.
    """
    if request.method == 'GET':
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
        
        today_date = datetime.now().date()
        yesterday_date = today_date - timedelta(days=1)
        
        # Create a dictionary containing information about the current tchat
        context = {
            'post_count': int(post_count),
            'latest_post_date': str(latest_post_date),
            'latest_post': str(latest_post),
            'tchat_slug_category': tchat_selected.slug_tchat_category,
            'tchat_slug_name': tchat_selected.slug_tchat_name,
            'today_date': today_date,
            'yesterday_date': yesterday_date,
        }
        
        return JsonResponse(context)
    
    else :
        context = None
        return JsonResponse(context)
 
    

