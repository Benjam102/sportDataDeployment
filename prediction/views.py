# Model import
from .models import predictions_matches
from website.models import matches

# Useful library
from django.http import JsonResponse


def prediction_match(request, slug_match) :
    """
    View function that allows us to register the prediction of a user.

    Parameters:
        request (HttpRequest): The HTTP request object.
        slug_match: Id of the match for the prediction.

    Returns:
        JsonResponse: 1. If the request method is 'POST', it returns a JSON response with details on the prediction.
                      2. If the request method is not 'POST', it returns a JSON response which is equal to none.
    """
    if request.method == 'POST':
        margin = request.POST.get('margin')
        total = request.POST.get('total')
        button = request.POST.get('button')
        user = request.user

        match = matches.objects.get(key_id = slug_match)
        verification = predictions_matches.objects.filter(prediction_match=match, user_prediction=user)
        
        # First prediction -> creation of the table
        if button == 'button1' :            
            if not verification.exists() :
                predictions_matches.objects.create(
                    prediction_match=match, user_prediction=user, prediction_margin1=margin, prediction_margin2=None,
                    prediction_total1=total, prediction_total2=None)

        # Second prediction 
        elif button == 'button2' :
            # Case where the user has not made a first prediction
            if not verification.exists() :
                predictions_matches.objects.create(
                    prediction_match=match, user_prediction=user, prediction_margin1=None, prediction_margin2=margin,
                    prediction_total1=None, prediction_total2=total)
            
            # Case where the user has made a first prediction -> just add the second prediction on the table previously created
            elif verification.prediction_margin2 :
                prediction = predictions_matches.objects.get(prediction_match=slug_match, user_prediction=user)
                prediction.prediction_margin2 = margin
                prediction.prediction_total2 = total

                prediction.save()
        
        context = {
            'margin': margin,
            'total': total,
            'button': button,
        }
            
        return JsonResponse(context)
    
    else :
        context = None
        return JsonResponse(context)
