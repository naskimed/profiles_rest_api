# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from rest_framework import status
# Create your views here.

class HelloApiView(APIView):
    """Test API View"""

    serializer_class = serializers.HelloSerializer

    def get(self,request,format=None):
        """Return a list of APIView featuers."""

        an_apiview = [
            'Uses HTTP methods as function(get,post,patch,put,delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello', 'an_apiview':an_apiview})
    
    def post(self,request):
        """Create a hello message with our name."""

        serializer = serializers.HelloSerializer(data = request.data) #from a JSON request to a python object 

        if serializer.is_valid():
            name = serializer.data.get('name')
            email = serializer.data.get('email')
            message = 'Hello {0} /nYour email is {1}'.format(name,email)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,pk = None):
        """Handles updating an object"""

        return Response({'method': 'put'})
    

    def patch(self, request, pk = None):
        """Patch request, only updates fields provided in the request."""

        return Response({'method': 'patch'})
    
    def delete(self, request, pk = None):
        """delete request, only delete fields provided in the request."""

        return Response({'method': 'delete'})
    

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet."""

    serializer_class = serializers.HelloSerializer

    def list(self,request):
        """Return a hello message."""

        a_viewset = [
            'Uses actions (list,create,retrieve,update,partial_update)',
            'Automatically maps to URLs using Rootes',
            'Provides more functionality with less code'
        ]

        return Response({'message':'Hello!','a_viewset':a_viewset})
    
    def create(self,request):
        """Create a new hello message"""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self,request,pk=None):
        """Handels getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self,request,pk=None):
        """Handels updating an object"""

        return Response({'http_method': 'PUT'})
    
    def partial_update(self,request,pk=None):
        """Handels updating part of an object"""

        return Response({'http_method':'PATCH'})

    def destroy(self,request,pk=None):
        """Handels romeving an object"""

        return Response({'http_method':'DELETE'})

    

