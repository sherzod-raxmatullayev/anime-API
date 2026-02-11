# urls.py
from django.urls import path
from .views import AnimeEpisodesListView, AnimeViewSet, EpisodeVideoStreamView, SavedAnimeToggleView
from rest_framework.routers import DefaultRouter
from .views import SavedAnimeListCreateView, SavedAnimeDeleteView
router = DefaultRouter()
router.register(r"animes", AnimeViewSet, basename="animes")

urlpatterns = [
    # custom endpointlar
    path("animes/<int:anime_id>/episodes/", AnimeEpisodesListView.as_view(), name="anime-episodes"),
    path("episodes/<int:pk>/video/", EpisodeVideoStreamView.as_view(), name="episode-video"),
    path("saved-animes/", SavedAnimeListCreateView.as_view(), name="saved_anime_list_create"),
    path("saved-animes/<int:anime_id>/", SavedAnimeDeleteView.as_view(), name="saved_anime_delete"),
    path("saved-animes/<int:anime_id>/toggle/", SavedAnimeToggleView.as_view(), name="saved_anime_toggle"),
]

# router endpointlarni qo‘shamiz
urlpatterns += router.urls


'''GET /api/animes/
GET /api/animes/?search=naruto
GET /api/animes/12/
'''
