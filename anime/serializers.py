# serializers.py
from os import read
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

class EpisodeSerializer(serializers.ModelSerializer):
    anime_id = serializers.IntegerField(source='anime.id', read_only=True)
    anime_title = serializers.CharField(source='anime.title', read_only=True)
    video_url = serializers.SerializerMethodField()
    video_size = serializers.SerializerMethodField()

    class Meta:
        model = Episode
        fields = [
            "id",
            "anime_id",
            "anime_title",
            "episode_number",
            "video",
            "video_url",
            "video_size",
            "created_at",
            "updated_at",
        ]

    def get_video_url(self, obj):
        if not obj.video:
            return None
        request = self.context.get("request")
        url = obj.video.url
        return request.build_absolute_uri(url) if request else url

    def get_video_size(self, obj):
        # modeldagi get_video_size() ishlatamiz
        return obj.get_video_size()