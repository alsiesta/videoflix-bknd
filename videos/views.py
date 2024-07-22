from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Video, Favorite


def all_videos(request):
    videos = Video.objects.all()
    video_list = []
    for video in videos:
        video_data = {
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'created_at': video.created_at,
            'categories': list(video.categories.values('id', 'name'))
        }
        video_list.append(video_data)
    return JsonResponse(video_list, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request, video_id):
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
    favorites = Favorite.objects.filter(user=request.user).select_related('video')
    favorite_videos = [{'id': fav.video.id, 'title': fav.video.title, 'description': fav.video.description} for fav in favorites]
    return Response(favorite_videos)