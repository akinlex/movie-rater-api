from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, RatingViewSet, MUserViewSet

# Create your views here.
router = DefaultRouter()
router.register('movies', MovieViewSet, basename='movies_api')
router.register('ratings', RatingViewSet, basename='ratings_api')
router.register('users', MUserViewSet, basename='users_api')

urlpatterns = router.urls