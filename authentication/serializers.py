from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from authentication.models import Area,User_Personal,Album,Track
from rest_framework.validators import UniqueValidator

class UserProfileSerializer(serializers.ModelSerializer):

    mobileno = serializers.CharField(validators=[UniqueValidator(queryset=User_Personal.objects.all())])


    class Meta:
        model = User_Personal
        fields = ('id','mobileno','area')


    # def create(self, validated_data):
    #
    #         user_data = validated_data.pop('user')
    #         user = UserSerializer.create(UserSerializer(), validated_data=user_data)
    #         user_info = User_Personal.objects.create(user=user,
    #                                                  mobileno=validated_data.pop('mobileno'),area=validated_data.pop('mobileno'))
    #         return user_info



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=5)
    user_profile=UserProfileSerializer()


    def create(self, validated_data):
        user_profile = validated_data.pop('user_profile')

        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        user.set_password(validated_data['password'])
        user.first_name=validated_data['first_name']
        user.last_name=validated_data['last_name']
        user.save()

        User_Personal.objects.create(user=user,**user_profile)

        return user



    class Meta:
        model = User
        fields = ('id', 'username','first_name','last_name', 'email', 'password','user_profile')






class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('order', 'title', 'duration')

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'tracks')

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album