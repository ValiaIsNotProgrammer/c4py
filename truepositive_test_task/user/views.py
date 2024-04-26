from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User


class CreateUserAPIView(APIView):

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_exists = User.objects.filter(user_id=user_id).exists()
        if user_exists:
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        new_user = User.objects.create(user_id=user_id)
        return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)
