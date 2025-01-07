from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.conf import settings
import markdown
from django.utils.safestring import mark_safe

#retrieve the user model defined in AUTH_USER_MODEL
User = get_user_model()

# Organizes blog posts into categories with a unique name
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name'] #categories are displayed in alphabetical order

    def __str__(self):
        return self.name

#optional for labelling blog posts with a unique name  
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name'] # Tags are displayed in alphabetical order

    def __str__(self):
        return self.name

# represents individual blog posts  
class BlogPost(models.Model):
    #choices for the status of the blog post
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")# Author of the post- deletes when the author is deleted
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) # Sets to null if category is deleted
    published_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True) #Auto-set on creation
    tags = models.ManyToManyField(Tag, blank=True)# tags associated with the post
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='draft')


    @property
    def content_as_html(self):
        """
        convert Markdown content of the blog post into HTML for safe rendering
        """
        return mark_safe(markdown.markdown(self.content))
    
    def publish(self):
        """
        Publish the post by setting its status to 'published' 
        and updating the published_date.
        """
        self.status = 'published'
        self.published_date=now()
        self.save()

    class Meta:
        ordering = ['-published_date'] # Display the most recent posts first


    def __str__(self):
        return self.title
    
#user comments on blog posts   
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)# user who authored the comment
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date'] #Display the most recent comments first


    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"
    
# Likes on blog posts    
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')# Ensures a user can like a post only once
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
    
# rating blog posts
class PostRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)])# Rating value between 1 and 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post') # Ensures a user can rate a post only once
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} rated {self.post.title} with {self.rating}"

# subscriptions to authors
class AuthorSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')# subscriber
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')# Subscribed author
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'author')# ensures a user can subscribe to an author only once
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"{self.user.username} subscribed to {self.author.username}"

# notifications for blog posts   
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username} - Read: {self.is_read}"