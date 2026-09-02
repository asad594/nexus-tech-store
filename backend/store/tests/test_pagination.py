from django.test import TestCase
from store.pagination import (
    NexusStandardPagination,
    NexusCompactPagination,
    NexusLargePagination,
)

class PaginationConfigurationTestCase(TestCase):
    def test_standard_pagination_defaults(self):
        paginator = NexusStandardPagination()
        self.assertEqual(paginator.page_size, 12)
        self.assertEqual(paginator.max_page_size, 100)
        self.assertEqual(paginator.page_size_query_param, 'page_size')

    def test_compact_pagination_defaults(self):
        paginator = NexusCompactPagination()
        self.assertEqual(paginator.page_size, 6)
        self.assertEqual(paginator.max_page_size, 24)

    def test_large_pagination_defaults(self):
        paginator = NexusLargePagination()
        self.assertEqual(paginator.page_size, 50)
        self.assertEqual(paginator.max_page_size, 250)
