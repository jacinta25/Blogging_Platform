import django_filters
from blog.models import BlogPost

class BlogPostFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='published_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='published_date', lookup_expr='lte')

    class Meta:
        model = BlogPost
        fields = ['category', 'author', 'status', 'start_date', 'end_date']
