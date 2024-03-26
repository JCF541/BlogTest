from rest_framework import status,generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from .models import UserProfile
from .serializers import UserProfileSerializer

class HomeView(APIView):
    """
    View to return a simple homepage message.
    """

    def get(self, request, format=None):
        content = {'message': 'Welcome to TESTBLOG!'}
        return Response(content)

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Override the default get_object method to return the profile
        of the currently authenticated user.
        """
        user = self.request.user
        return get_object_or_404(UserProfile, user=user)

    def update(self, request, *args, **kwargs):
        """
        Override the default update method to provide custom behavior.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)