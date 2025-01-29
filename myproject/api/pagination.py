# api/pagination.py
from rest_framework.pagination import PageNumberPagination

class StandardResultsPagination(PageNumberPagination):
    # Custom pagination class for flexible page size and control
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow clients to customize the page size
    max_page_size = 100  # Maximum allowed page size to prevent large requests

    def get_paginated_response(self, data):
        # Customize paginated response to include metadata like total count
        return super().get_paginated_response({
            'count': self.page.paginator.count,  # Total number of objects
            'next': self.get_next_link(),  # Link to the next page
            'previous': self.get_previous_link(),  # Link to the previous page
            'results': data  # The actual data for this page
        })
