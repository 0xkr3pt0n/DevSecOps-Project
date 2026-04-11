from django.http import JsonResponse

x = 3

def home(request):
    return JsonResponse({
        "message": "Hello world",
        "API_KEY": "SECRET_123"
    })

home("asdasdassa")