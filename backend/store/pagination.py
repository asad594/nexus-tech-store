"""
Configurable Page-Number Pagination Classes
Allows frontend clients to customize page sizes dynamically via query parameters.
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class NexusStandardPagination(PageNumberPagination):
    """
    Standard pagination class for Nexus Tech Store endpoints.
    Defaults to 12 items, max 100 items per request.
    """
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class NexusCompactPagination(PageNumberPagination):
    """
    Compact pagination class for carousels, related items, and quick previews.
    Defaults to 6 items per page.
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 24
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class NexusLargePagination(PageNumberPagination):
    """
    Large dataset pagination for admin exports, logs, and bulk catalog views.
    Defaults to 50 items, max 250.
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 250
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

