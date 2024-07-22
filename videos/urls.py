from django.urls import path
from .views import all_videos, add_favorite, list_favorites

urlpatterns = [
	path('', all_videos, name='all_videos'),
	path('favorites/', list_favorites, name='list_favorites'),
 	path('add_favorite/<int:video_id>/', add_favorite, name='add_favorite'),
    path('list_favorites/', list_favorites, name='list_favorites'),
]