from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.apps import apps

@api_view(['POST'])
def spam_check(request):
    # Treść z JSON-a: np. {"email_text": "Hello..."}
    text = request.data.get('email_text', '')
    
    print(text)

    # Pobieramy nasz classifier z ApiConfig
    api_config = apps.get_app_config('api')  # nazwa klasy w apps.py -> ApiConfig
    classifier = api_config.spam_classifier

    # Predykcja
    label = classifier.predict(text)
    # label = 1 -> spam, 0 -> ham
    result = "spam" if label == 1 else "ham"

    return Response({"result": result})
