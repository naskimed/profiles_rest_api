# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from rest_framework import status

from . import models
from . import permission
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
# Create your views here.
"""
class HelloApiView(APIView):

    serializer_class = serializers.HelloSerializer

    def get(self,request,format=None):

        an_apiview = [
            'Uses HTTP methods as function(get,post,patch,put,delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello', 'an_apiview':an_apiview})
    
    def post(self,request):

        serializer = serializers.HelloSerializer(data = request.data) #from a JSON request to a python object 

        if serializer.is_valid():
            name = serializer.data.get('name')
            email = serializer.data.get('email')
            message = 'Hello {0} /nYour email is {1}'.format(name,email)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,pk = None):

        return Response({'method': 'put'})
    

    def patch(self, request, pk = None):

        return Response({'method': 'patch'})
    
    def delete(self, request, pk = None):
    
        return Response({'method': 'delete'})
"""
"""
class HelloViewSet(viewsets.ViewSet):

    serializer_class = serializers.HelloSerializer

    def list(self,request):
        a_viewset = [
            'Uses actions (list,create,retrieve,update,partial_update)',
            'Automatically maps to URLs using Rootes',
            'Provides more functionality with less code'
        ]

        return Response({'message':'Hello!','a_viewset':a_viewset})
    
    def create(self,request):
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self,request,pk=None):
        return Response({'http_method': 'GET'})

    def update(self,request,pk=None):
        return Response({'http_method': 'PUT'})
    
    def partial_update(self,request,pk=None):
        return Response({'http_method':'PATCH'})

    def destroy(self,request,pk=None):
        return Response({'http_method':'DELETE'})
"""
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfiles.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)