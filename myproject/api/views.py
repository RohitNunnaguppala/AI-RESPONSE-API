import time
from rest_framework import viewsets, status
from rest_framework.response import Response as DRFResponse
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters import rest_framework as filters
from rest_framework.throttling import UserRateThrottle
from .models import Response
from .serializers import ResponseSerializer
from .exceptions import BadRequestException

# Filter class for date range and model-based filtering
class ResponseFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Response
        fields = ['model_used', 'status']

# Viewset for handling responses
class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ResponseFilter
    throttle_classes = [UserRateThrottle]  # Apply rate limiting

    # Caching for the response listing (caches the entire response list)
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # Create a new response and simulate AI model processing
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Simulate AI model processing (this should be replaced with actual model logic)
            start_time = time.time()
            response_text = f"Sample response for prompt: {serializer.validated_data['prompt']}"
            processing_time = time.time() - start_time
        except Exception as e:
            raise BadRequestException(f"AI Model Error: {str(e)}")

        # Create the Response object and save it to the database
        response = Response.objects.create(
            prompt=serializer.validated_data['prompt'],
            response_text=response_text,
            model_used=serializer.validated_data['model_used'],
            status='completed',
            processing_time=processing_time
        )

        result_serializer = self.get_serializer(response)
        return DRFResponse(result_serializer.data, status=status.HTTP_201_CREATED)

    # Override the default queryset to use caching for filtered results
    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = str(self.request.query_params)  # Include query parameters in cache key

        # Include both user ID and query parameters to form a unique cache key
        cache_key = f'response_queryset_{self.request.user.id}_{filter_params}'

        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset

        # Apply filters from request query parameters
        queryset = queryset.filter(**self.request.query_params.dict())
        cache.set(cache_key, queryset, timeout=300)  # Cache for 5 minutes
        return queryset