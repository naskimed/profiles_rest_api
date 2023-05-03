from rest_framework import serializers
from . import models

class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer fo the user profile objects"""

    class Meta:
        model = models.UserProfiles
        fields = ('id','email','name','password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        """Create and return new user"""

        user = models.UserProfiles(
            email = validated_data['email'],
            name = validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class SubjectSerializer(serializers.ModelSerializer):
    """A serializer for the subjects"""

    class Meta:
        model = models.Subject
        fields = ('id','Subname','description')
    
    def create(self,validated_data):
        """Create and return a subject"""

        subject = models.Subject(
            Subname = validated_data['Subname'],
            description = validated_data['description']
        )
        subject.save()
        return subject
    

class GroupSerializer(serializers.ModelSerializer):
    """A serializer for the Groups"""
    subject = serializers.PrimaryKeyRelatedField(queryset=models.Subject.objects.all())

    class Meta: 
        model = models.Group
        fields = ('id','name', 'description','subject')

    def create(self,validated_data):

        
        subject_data = validated_data.pop('subject')
        subject = models.Subject.objects.get(id=subject_data.id)
        group = models.Group.objects.create(subject=subject, **validated_data)

        group.save()
        return group

