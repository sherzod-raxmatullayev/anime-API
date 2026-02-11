from django.shortcuts import render
from yaml import serialize
from .serializers import UserSerializer, RegisterSerializer


from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'message':'User Created', 'user':UserSerializer(user).data},
            status=status.HTTP_201_CREATED )
    
class ProfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status = status.HTTP_200_OK)
    
'''{
  "username": "sherzod_dev",
  "email": "sherzod@example.com",
  "password": "strongpass123",
  "first_name": "Sherzod",
  "last_name": "Raxmatullayev"
}
'''
