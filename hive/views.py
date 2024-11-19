from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Post, Hashtag, LikedUsers, FollowedHashtags, LikedPosts
from .serializers import (
    UserSerializer, PostSerializer, HashtagSerializer,
    LikedUsersSerializer, FollowedHashtagsSerializer, LikedPostsSerializer
)
from django.db.models import Q  # Tarvitaan monimutkaisempia kyselyitä varten

# Create viewsets for each model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # All users
    serializer_class = UserSerializer  # Use the User serializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-time')  # All posts, ordered by time (newest first)
    serializer_class = PostSerializer  # Use the Post serializer
    
    # Enable filtering using DjangoFilterBackend
    filter_backends = [DjangoFilterBackend]
    
    # Suodatus 'hashtags' id:n perusteella
    filterset_fields = ['hashtags__id']  # Filter posts by the hashtag id

    # Custom action for filtering posts by multiple hashtags
    @action(detail=False, methods=['get'], url_path='filter-by-hashtags')
    def filter_by_hashtags(self, request):
        # Get the 'hashtags' query parameter (a list of hashtag IDs)
        hashtag_ids = request.query_params.getlist('hashtags', None)
        
        if not hashtag_ids:
            return Response({'error': 'At least one hashtag ID is required.'}, status=400)
        
        # Try to convert hashtag_ids to integers
        try:
            hashtag_ids = [int(id) for id in hashtag_ids]
        except ValueError:
            return Response({'error': 'Each hashtag ID must be a valid integer.'}, status=400)
        
        # Query posts that match any of the provided hashtag IDs
        posts = Post.objects.filter(hashtags__id__in=hashtag_ids).distinct()
        
        # Serialize and return the filtered posts
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()  # All hashtags
    serializer_class = HashtagSerializer  # Use the Hashtag serializer

class LikedUsersViewSet(viewsets.ModelViewSet):
    queryset = LikedUsers.objects.all()  # All liked users
    serializer_class = LikedUsersSerializer  # Use the LikedUsers serializer

    # Functionality for http://127.0.0.1:8000/liked-users/count-likes/?user_id=X
    # Get to know how many users you liked.
    @action(detail=False, methods=['get'], url_path='count-likes')
    def count_likes(self, request):
        # Get the user_id from query parameters
        user_id = request.query_params.get('user_id', None)
        if user_id is None:
            return Response({'error': 'user_id parameter is required.'}, status=400)
        
        # Validate user_id as an integer
        try:
            user_id = int(user_id)
        except ValueError:
            return Response({'error': 'user_id must be a valid integer.'}, status=400)
        
        # Count how many users the specified user has liked
        liked_count = LikedUsers.objects.filter(liker=user_id).count()
        return Response({'user_id': user_id, 'liked_count': liked_count})

    # Functionality for http://127.0.0.1:8000/liked-users/count-liked-by/?user_id=X
    # Get to know how many users likes you.
    @action(detail=False, methods=['get'], url_path='count-liked-by')
    def count_liked_by(self, request):
        # Get the user_id from query parameters
        user_id = request.query_params.get('user_id', None)
        if user_id is None:
            return Response({'error': 'user_id parameter is required.'}, status=400)
        
        # Validate user_id as an integer
        try:
            user_id = int(user_id)
        except ValueError:
            return Response({'error': 'user_id must be a valid integer.'}, status=400)
        
        # Count how many users have liked the specified user
        liked_by_count = LikedUsers.objects.filter(liked_user=user_id).count()
        return Response({'user_id': user_id, 'liked_by_count': liked_by_count})

class FollowedHashtagsViewSet(viewsets.ModelViewSet):
    queryset = FollowedHashtags.objects.all()  # All followed hashtags
    serializer_class = FollowedHashtagsSerializer  # Use the FollowedHashtags serializer

class LikedPostsViewSet(viewsets.ModelViewSet):
    queryset = LikedPosts.objects.all()  # All liked posts
    serializer_class = LikedPostsSerializer  # Use the LikedPosts serializer
