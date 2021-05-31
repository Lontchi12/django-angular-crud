# from auth.users.serializers import UserSerializer
from django.http import response
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import TodoSerializer, UserSerializer
from django.contrib.auth.decorators import login_required
from .models import User, Todo
import jwt, datetime

# Create your views here.

class ResgisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        jwt.decode(token, "secret", algorithms=["HS256"])


        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthorized')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthorized')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "Success"
        }

        return response



class TodoView(APIView):
    # @login_required
    # permission_classes = (IsAuthenticated,)
    # authentication_class = TokenAuthentication
    def get(self, request):

        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many = True)
        return Response(serializer.data)

class TodoDetailView(APIView):
    
    def get(self, request, pk):
        todos = Todo.objects.get(id=pk)
        serializer = TodoSerializer(todos, many=False)
        return Response(serializer.data)


class TodoCreateView(APIView):
    
    def post(self, request):
        serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class TodoUpdateView(APIView):
    
    authentication_class = TokenAuthentication
    def put(self, request, pk):
        todo = Todo.objects.get(id=pk)
        serializer = TodoSerializer(instance=todo, data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class TodoDeleteView(APIView):
    
    def delete(self, request,pk):
        todo = Todo.objects.get(id=pk)
        todo.delete()

        return Response("Todo Successfully Deleted")









        
