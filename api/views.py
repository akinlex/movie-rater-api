from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .models import Movie, Rating, Cast, MUser, CustomUser
from .serializers import MovieSerializer, RatingSerializer, CastSerializer, MUserSerializer, MovieMiniSerializer
from .utils import max_min_validator

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieMiniSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    # Rate movie 
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        # Check if starts is passed as a request
        if 'stars' in request.data:
            # Prepare rating object data
            movie = get_object_or_404(Movie, id=pk)
            stars = int(request.data['stars'])
            star_rating = max_min_validator(stars)
            logged_in_user = request.user.id
            user = get_object_or_404(MUser, id=logged_in_user)

            print(logged_in_user)

            '''
            get_or_create()
            This method is atomic assuming that the database enforces uniqueness of the keyword 
            arguments (see unique or unique_together). If the fields used in the keyword arguments
            do not have a uniqueness constraint, concurrent calls to this method may result in 
            multiple rows with the same parameters being inserted.

            '''

            # Get rating if exists or create new
            rating, created = Rating.objects.get_or_create(user=user, stars=star_rating, movie=movie)
            # rating.stars = stars
            # rating.save()

            # Serialize data and pass as response
            serializer = RatingSerializer(rating, many=False)
            response = {'message': 'Success!', 'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)       
        else:
            response = {'message': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MovieSerializer(instance)
        return Response(serializer.data)
        instance = self.get

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Restrict default methods from creating and updating model
    def update(self, request, *args, **kwargs):
        response = {'message': 'Sorry! You cant update rating'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'Sorry! You cant create rating'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = MUserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


