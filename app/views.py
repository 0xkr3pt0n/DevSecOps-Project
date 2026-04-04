from django.http import JsonResponse



def home(request):
    return JsonResponse({
        "message": "Hello world",
        "API_KEY": "SECRET_123"
    })

