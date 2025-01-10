from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from blog.models import BlogPost, Category, Tag, Comment, PostLike, PostRating, AuthorSubscription, Notification
from .serializers import BlogPostSerializer, CategorySerializer, TagSerializer, UserSerializer, CommentSerializer, AuthorSubscriptionSerializer,NotificationSerializer, PostLikeSerializer, PostRatingSerializer
from .filters import BlogPostFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.db import models
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Custom action to handle user registration
    @action(detail=False, methods=['post'], url_path='register', permission_classes=[])
    def register(self, request):
        # Get data from the request
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username', '')
        bio = request.data.get('bio', '')
        

        # Validate the input data
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Use the serializer to create the user
        user_data = {
            'email': email,
            'password': password,
            'username': username,
            'bio': bio
            
        }
        serializer = UserSerializer(data=user_data)

        # Validate and save the user
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully.",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Allows a user to subscribe to another user(author)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe_to_author(self, request, pk=None):
        author = self.get_object() #Get author to subscribe to

        #check if the user is already subscribed to the author
        if AuthorSubscription.objects.filter(user=request.user, author=author).exists():
            #if subscription exits return error message
            return Response({"detail": "Already subscribed to this author."}, status=status.HTTP_400_BAD_REQUEST)
        
        #If the subscription does not exist, create a new subscription
        subscription = AuthorSubscription.objects.create(user=request.user, author=author)

        #Notify the user that they have succesfully subscribed
        notification = Notification.objects.create(user=request.user, message=f"Successfully subcribed to {author.username}.")
        notification_serializer = NotificationSerializer(notification)

        #return a success response (resource created)
        return Response({
            'subscription' :AuthorSubscriptionSerializer(subscription).data,
            'notification' :notification_serializer.data
            }, status=status.HTTP_201_CREATED)


    #Allows a user to unsubscribe from another user(author
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unsubscribe_from_author(self, request, pk=None):
        author = self.get_object()
        
        # Try to find an existing subscription for this author and user
        subscription = AuthorSubscription.objects.filter(user=request.user, author=author).first()
        
        #if no subscription is found return error message
        if not subscription:
            return Response({"detail": "You are not subscribed to this author."}, status=status.HTTP_400_BAD_REQUEST)
        
        #if subscription exists, delete it
        subscription.delete()

        #Notify the user that they have already unsubscribed
        notification = Notification.objects.create(user=request.user, message=f"Successfully unsubscribed from {author.username}")
        notification_serializer = NotificationSerializer(notification)


        return Response({
            "detail": "Successfully unsubscribed from the author.",
            'notification' : notification_serializer.data
            }, status=status.HTTP_204_NO_CONTENT)

class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    #ensure that only authenticated(logged-in) users can access these views and IsOwnerOrReadOnly restricts modification to the owner
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    #filtering options
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] # adds search, filter and ordering capabilities
    filterset_class = BlogPostFilter
    filterset_fields = ['category', 'author', 'status', 'published_date']
    
    #searching and ordering
    search_fields = ['title', 'content', 'tags__name', 'author__username']
    ordering_fields = ['published_date', 'title']

    #Override the perform_create method to automatically associate the post with the currently authenticated user
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)# save the blog post with the author as the currently authenticated user 

    #Overide perform_update to restrict updating a blog post to the post's owner
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:# Check if the authenticated user is the author of the post
            raise PermissionDenied("You cannot update another user's post.") #raise an error if the user is not the author
        serializer.save() # save the updated blog post

    #Override the perform_destroy to restrict deleting a blog post to the post's owner
    def perform_destroy(self, instance):
        if instance.author != self.request.user:# ensure only the author can delete their own post
            raise PermissionDenied("You cannot delete another user's post.")
        instance.delete()#delete the post


# Custom action to get blog posts filtered by category
    @action(detail=False, methods=['get'], url_path='category/(?P<category_name>[^/.]+)')
    def posts_by_category(self, request, category_name=None):
        if not category_name:# Check if the category name is provided in the URL
            raise ValidationError("Category name is required.") # Raise a validation error if missing
        try:
            category = Category.objects.get(name=category_name) #try to find the category by name
        except Category.DoesNotExist:
            raise NotFound("Category not found.")
        
        #Retrieve posts belonging to this category with optimized queries for author and tags
        posts = BlogPost.objects.filter(category=category)
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

#Custom action to get blog posts by a specific author
    @action(detail=False, methods=['get'], url_path='author/(?P<author_username>[^/.]+)')
    def posts_by_author(self, request, author_username=None):
        if not author_username:
            raise ValidationError("Author username is required.")
        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            raise NotFound("Author not found.")
        
        #retrieve posts by this author with optimized queries for category and tags
        posts = BlogPost.objects.filter(author=author)
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)
    
 
# Custom action to like a blog post
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like_post(self, request, pk=None):
        post = self.get_object()# Get post using the provided primary key(pk)

        # Check if the user has already liked the post
        if PostLike.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        #if the user hasn't like the post , create a like record
        PostLike.objects.create(user=request.user, post=post)
        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)
# Custom action to rate a blog post
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rate_post(self, request, pk=None):
        post = self.get_object()
        rating_value = request.data.get('rating')# get the rating value from the request
        
        #ensure the rating is valid(between 1 and 5)
        if not rating_value or not (1 <= int(rating_value) <= 5):
            return Response({"detail": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)
        
        #update or create the rating record
        rating, created = PostRating.objects.update_or_create(
            user=request.user, post=post, defaults={'rating': rating_value})
        return Response({"detail": f"Post rated successfully with {rating_value}."}, status=status.HTTP_200_OK)

#custom action to check the average rating for each post
    @action(detail=False, methods=['get'])
    def most_liked(self, request):
        #uses annotate to calculate the average rating for each post
        # Orders posts by their average rating in descending order
        most_liked_posts = BlogPost.objects.annotate(likes_count=models.Count('postlike')).order_by('-likes_count')
        serializer = BlogPostSerializer(most_liked_posts, many=True)
        return Response(serializer.data)

#custom action for value of how the blog post was rated
    @action(detail=False, methods=['get'])
    def highest_rated(self, request):
        highest_rated_posts = BlogPost.objects.annotate(average_rating=models.Avg('postrating__rating')).order_by('-average_rating')
        serializer = BlogPostSerializer(highest_rated_posts, many=True)
        return Response(serializer.data)
    

#custom action to share a post via email    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def share_post(self, request, pk=None):
        post = self.get_object()
        email = request.data.get('email')

        #check if email is provided
        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use Django's send_email function to send the post content via email
            send_mail(
                subject=f"Check out this blog post: {post.title}",
                message=post.content,
                from_email='no-reply@blog.com',
                recipient_list=[email],
            )
            return Response({"detail": "Post shared successfully."}, status=status.HTTP_200_OK)

        except Exception as e:# if there is an error while sending the email
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]  # Optional: Only allow authenticated users to create/edit tags.

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().select_related('author', 'post')  # Optimize with select_related
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

#assigns the currently authenticated user as the author of the comment
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#Ensures that only thr comment's author can update it.
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You cannot update another user's comment.")
        serializer.save()

#Ensures that only the comment's author can delete it.
    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You cannot delete another user's comment.")
        instance.delete()

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        # Validate the input
        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check the password
        if not user.check_password(password):
            return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate and return the token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "access": access_token,
            "refresh": str(refresh)
        })
