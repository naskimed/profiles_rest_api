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
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions
from django.shortcuts import render, get_object_or_404
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
    permission_classes = (permission.UpdateOwnProfile,permissions.IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return models.UserProfiles.objects.all()
        else:
            return models.UserProfiles.objects.filter(pk =self.request.user.pk)
            
    
    def create(self, request):
        serializer = serializers.UserProfileSerializer(data=request.data)
        if self.request.user.is_staff and serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
        except models.UserProfiles.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if self.request.user.is_staff or instance.name == self.request.user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Only staff members or the user that owns the profile are allowed to delete it.'},
                            status=status.HTTP_403_FORBIDDEN)


class LoginViewSet(viewsets.ViewSet):
    """Checks email and password"""

    serializer_class = AuthTokenSerializer

    def create(self,request):
        """Use the ObtainAuthtoken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)
        
        
class SubjectsViewSet(viewsets.ViewSet):
    """Manage the subjects"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.SubjectSerializer
    queryset = models.Subject.objects.all()

    def get_queryset(self):
        return models.Subject.objects.all()
    
    def list(self, request):
        subjects = self.get_queryset()
        serializer = serializers.SubjectSerializer(subjects, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        serializer = serializers.SubjectSerializer(data=request.data)
        if self.request.user.is_staff and serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        subject = get_object_or_404(models.Subject, pk=pk)
        serializer = serializers.SubjectSerializer(subject)
        return Response(serializer.data)

    def subject_list_view(request):
        subjects = models.Subject.objects.all()
        return render(request, 'subjects/subject_list.html', {'subjects': subjects})

    def subject_detail_view(request, pk):
        subject = get_object_or_404(models.Subject, pk=pk)
        return render(request, 'subjects/subject_detail.html', {'subject': subject})
    
    def destroy(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
        except models.Subject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if self.request.user.is_staff:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Only staff members or the user that owns the profile are allowed to delete it.'},
                            status=status.HTTP_403_FORBIDDEN)
    

class GroupViewSet(viewsets.ViewSet):
    """Manage the subjects"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()

    def get_queryset(self):
        return models.Group.objects.all()
    
    def list(self, request):
        subjects = self.get_queryset()
        serializer = serializers.GroupSerializer(subjects, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        serializer = serializers.GroupSerializer(data=request.data)
        if self.request.user.is_staff and serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        subject = get_object_or_404(models.Group, pk=pk)
        serializer = serializers.GroupSerializer(subject)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
        except models.Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if self.request.user.is_staff:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Only staff members or the user that owns the profile are allowed to delete it.'},
                            status=status.HTTP_403_FORBIDDEN)