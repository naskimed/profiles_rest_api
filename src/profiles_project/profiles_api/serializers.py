from rest_framework import serializers
from . import models

"""
class HelloSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=10)  #This is the field in the admin server 
"""


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


