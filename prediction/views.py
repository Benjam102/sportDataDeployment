from django.shortcuts import render
from .models import predictions_matches
from django.http import JsonResponse

from website.models import matches
# Create your views here.

def predictionMatch(request, slug_match) :
    if request.method == 'POST':
        margin = request.POST.get('margin')
        total = request.POST.get('total')
        button = request.POST.get('button')
        user = request.user

        match = matches.objects.get(key_id = slug_match)
        verification = predictions_matches.objects.filter(prediction_match=match, user_prediction=user)
        
        if button == 'button1' :            
            if not verification.exists() :
                predictions_matches.objects.create(
                    prediction_match=match, user_prediction=user, prediction_margin1=margin, prediction_margin2=None,
                    prediction_total1=total, prediction_total2=None)

        elif button == 'button2' :
            if not verification.exists() :
                predictions_matches.objects.create(
                    prediction_match=match, user_prediction=user, prediction_margin1=None, prediction_margin2=margin,
                    prediction_total1=None, prediction_total2=total)
            elif verification.prediction_margin2 :
                prediction = predictions_matches.objects.get(prediction_match=slug_match, user_prediction=user)
                prediction.prediction_margin2 = margin
                prediction.prediction_total2 = total

                prediction.save()
        
        response = {
            'status': 'success',
            'margin': margin,
            'total': total,
            'button': button,
        }
            
        return JsonResponse(response)
    return JsonResponse({'status': 'failed'})
