from django.core.paginator import Paginator

class SimplePaginator(Paginator):
    def count(self):
        return 9999999999
