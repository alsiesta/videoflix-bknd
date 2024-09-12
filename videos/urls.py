from django.urls import path
from .views import all_videos, add_favorite, list_favorites, get_video_by_id

urlpatterns = [
	path('', all_videos, name='all_videos'),
    path('<int:video_id>/', get_video_by_id, name='get_video_by_id'),
	path('favorites/', list_favorites, name='list_favorites'),
 	path('', add_favorite, name='add_favorite'),
    path('list_favorites/', list_favorites, name='list_favorites'),
]