from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Avg

from api.models import Movie, Rating, User
from api.serializers import MovieSerializer, RatingSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = User.objects.get(id=1)
            try:
                rating = Rating.objects.get(user=user.id, movie=movie)
                rating.stars = stars
                rating.save()
                print('updated existing rating')
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except Rating.DoesNotExist:
                Rating.objects.create(user=user, movie=movie, stars=stars)
                print('created new rating')

            response = {'message': 'its working'}
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'you must provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def avg_movie_rating(self, request, pk=None):
        try:
            movie = Movie.objects.get(id=pk)
            movie_ratings = Rating.objects.filter(movie=movie)
        except Rating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            avg_movie_rating = movie_ratings.aggregate(Avg('stars'))['stars__avg']
            response = {'avg_rating': avg_movie_rating}
            return Response(response, status=status.HTTP_200_OK)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


def for_neta(request):
    return HttpResponse(status=500, content="very bad")