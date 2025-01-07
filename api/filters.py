import django_filters
from blog.models import BlogPost

class BlogPostFilter(django_filters.FilterSet):
    """
    A filter class for filtering 'BlogPost' objects based on specific criteria.
    allows filtering blog posts by
    -a range of publised dates(start_date, end_date)
    -Category, Author, and status
    """
    #filter posts publised on or after a given date
    start_date = django_filters.DateFilter(
        field_name='published_date',# the model to filter on
        lookup_expr='gte'# "Greater than or equal to" for start of date range
        )
    
    #filter posts published on or before a given date
    end_date = django_filters.DateFilter(
        field_name='published_date', # the model field to filter on
        lookup_expr='lte' # "Less than or equal to" for the end of date range
        )

    class Meta:
        """
        provides additional information about the filter:
        -specifies the model filter ('BlogPost')
        -defines the fields available for filtering
        """
        model = BlogPost #the model that this filter applies to
        fields = ['category', 'author', 'status', 'start_date', 'end_date']
