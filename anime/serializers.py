# serializers.py
from rest_framework import serializers
from .models import Animes, Episode, SavedAnime

class EpisodeListSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Episode
        fields = ["id", "episode_number", "video_url", "created_at", "updated_at"]

    def get_video_url(self, obj):
        request = self.context.get("request")
        # URL routing nomi bo'yicha generatsiya qilsak ham bo'ladi; bu yerda oddiy path:
        path = f"/anime/episodes/{obj.pk}/video/"
        return request.build_absolute_uri(path) if request else path
    
class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animes
        fields = ["id", "title", "descriptions", "episodes", "release_date", "image", "created_at", "updated_at"]



class SavedAnimeSerializer(serializers.ModelSerializer):
    anime = AnimeSerializer(read_only=True)
    anime_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = SavedAnime
        fields = ["id", "anime", "anime_id", "created_at"]