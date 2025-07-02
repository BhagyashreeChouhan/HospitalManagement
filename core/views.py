from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.
class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message":"Account created",
                "data": serializer.data
            }, status=201)
        return Response({
                "message":"Account not created",
                "data": serializer.data
            }, status=400)
    
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password = serializer.validated_data['password'])
            if user is None:
                return Response({
                "message":"Invalid credentials.",
                "data": {}
            }, status=401)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message":"Logijn successful",
                "token": token.key
            }, status=200)
        return Response({
                "message":"Keys missing or invalid data.",
                "data":serializer.errors
            }, status=400)
