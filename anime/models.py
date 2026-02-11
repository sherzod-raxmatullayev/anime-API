from email.mime import image
from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.conf import settings



class Animes(models.Model):
    title = models.CharField(max_length=200, verbose_name='Nomi')
    descriptions = models.TextField(verbose_name='Tavsif')
    episodes = models.IntegerField(verbose_name='Epizdlar soni')
    release_date = models.DateField(verbose_name='Chiqgan sana')
    image = models.ImageField(upload_to='imgs/', verbose_name='Rasim', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")
    
    class Meta:
        verbose_name = 'Anime'
        verbose_name_plural = 'Animelar'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

class Episode(models.Model):
    anime = models.ForeignKey(Animes, on_delete=models.CASCADE, related_name='episodeslar', verbose_name='Anime')
    episode_number = models.IntegerField(verbose_name='Epizod raqami')
    video = models.FileField(upload_to='episodes/videos/', verbose_name="Video fayl")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Epizod"
        verbose_name_plural = "Epizodlar"
        ordering = ['anime', 'episode_number']
        unique_together = ['anime', 'episode_number']

    def __str__(self):
        return f"{self.anime.title} - Epizod {self.episode_number}"
    
    def get_video_size(self):
        import os
        if self.video and os.path.exists(self.video.path):
            return os.path.getsize(self.video.path)
        return 0
    
class SavedAnime(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_animes_rel")
    anime = models.ForeignKey(Animes, on_delete=models.CASCADE, related_name="saved_by_rel")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "anime")
        ordering = ["-created_at"]

    # def __str__(self):
        # return f"{self.user_id} -> {self.anime_id}"