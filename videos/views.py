from django.conf import settings

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .models import Video

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .serializers import VideoSerializer


from .models import Video, Favorite

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_videos(request):
    """
    Retrieve all videos.

    Request:
        - Method: GET
        - Authentication: TokenAuthentication
        - Permissions: IsAuthenticated

    Response:
        - 200 OK: A list of all videos with their details.
    """
    videos = Video.objects.all()
    video_list = []
    for video in videos:
        video_data = {
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'created_at': video.created_at,
            'categories': list(video.categories.values('id', 'name')),
            'path': video.path,
            'imagepath': video.imagepath,
        }
        video_list.append(video_data)
    return JsonResponse(video_list, safe=False)

@cache_page(CACHE_TTL)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_video_by_id(request, video_id):
    """
    Retrieve a video by its ID.

    Request:
        - Method: GET
        - Authentication: TokenAuthentication
        - Permissions: IsAuthenticated
        - URL Parameters: 
            - video_id: ID of the video to retrieve.

    Response:
        - 200 OK: Video details if found.
        - 404 Not Found: If the video does not exist.
    """
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return Response({"detail": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = VideoSerializer(video)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request, video_id):
    """
    Add or remove a video from the user's favorites.

    Request:
        - Method: POST
        - Authentication: TokenAuthentication
        - Permissions: IsAuthenticated
        - URL Parameters: 
            - video_id: ID of the video to add or remove from favorites.

    Response:
        - 201 Created: If the video was added to favorites.
        - 200 OK: If the video was removed from favorites.
    """
    video = Video.objects.get(id=video_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, video=video)
    if created:
        return Response({'status': 'added'}, status=201)
    else:
        favorite.delete()
        return Response({'status': 'removed'}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    """
    List all favorite videos of the authenticated user.

    Request:
        - Method: GET
        - Authentication: TokenAuthentication
        - Permissions: IsAuthenticated

    Response:
        - 200 OK: A list of favorite videos with their details.
    """
    favorites = Favorite.objects.filter(user=request.user).select_related('video')
    favorite_videos = [{'id': fav.video.id, 'title': fav.video.title, 'description': fav.video.description} for fav in favorites]
    return Response(favorite_videos)