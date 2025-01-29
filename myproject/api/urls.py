# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResponseViewSet

# Create a router and register the ResponseViewSet
router = DefaultRouter()
router.register(r'responses', ResponseViewSet)

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
]
