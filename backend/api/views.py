from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def hello_world(request):
    """
    Prosty przykład function-based view z DRF.
    Obsługuje TYLKO metodę GET (dzięki ['GET'] w dekoratorze).
    """
    return Response({"message": "Hello from DRF function-based view!"})


@api_view(['POST'])
def spam_check(request):
    """
    Przyjmuje metodę POST z JSON-em w formacie:
    {
       "email_text": "Your message here"
    }
    """
    email_text = request.data.get('email_text', '')

    # Prosta logika: jeśli w treści jest 'win', to spam, inaczej ham
    if "win" in email_text.lower():
        result = "spam"
    else:
        result = "ham"

    return Response({"result": result}, status=status.HTTP_200_OK)
