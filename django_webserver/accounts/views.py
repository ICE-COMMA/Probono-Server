from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def id_duplicate_check(request):
    user_id = request.data.get('username', None)
    if user_id:
        if User.objects.filter(username=user_id).exists():
            return JsonResponse(
                {'message':'This ID is already in use.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return JsonResponse(
            {'message':'This ID is available.'},
            status=status.HTTP_200_OK
        )
    return JsonResponse(
        {'message':'ID is required.'},
        status=status.HTTP_400_BAD_REQUEST
    )
