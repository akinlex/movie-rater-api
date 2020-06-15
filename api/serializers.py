from rest_framework import serializers
from .models import Movie, Rating, Cast, CustomUser, MUser
from rest_framework.authtoken.models import Token


class MUserMiniSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MUser
        fields =['first_name', 'last_name']

class MUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
                        'first_name': {'required': True},
                        'last_name': {'required': True},
                        'password': {'write_only': True, 'required': True},
                        'id': {'read_only': True},
                        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        appuser, created = MUser.objects.get_or_create(user=user, first_name=validated_data['first_name'], 
                                                        last_name=validated_data['last_name'])
        Token.objects.create(user=user)
        return user

        # user = CustomUser(
        # email=validated_data['email']
        # )
        # user.set_password(validated_data['password'])
        # user.save()
        # return user

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['user', 'stars', 'movie']

class CastSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cast
        fields = ['name', 'awards_won', 'role_played']

class MovieSerializer(serializers.ModelSerializer):
    cast = CastSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['id', 'title', 'summary', 'director', 'genre', 'is_released', 'date_released',
         'movie_length', 'cast', 'num_of_ratings', 'avg_ratings']

class MovieMiniSerializer(serializers.ModelSerializer):
    cast = CastSerializer(many=True)
    class Meta:
        model = Movie
        fields =['id', 'title', 'summary', 'director', 'genre', 'num_of_ratings', 'avg_ratings', 'cast']


