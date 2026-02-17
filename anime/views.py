import mimetypes
from sre_constants import CH_LOCALE
# from tkinter.tix import STATUS
from xxlimited import Str
from django.shortcuts import render
import os
import re
from django.http import StreamingHttpResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404
import django_filters
from .models import Animes, Episode
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import generics
from .serializers import EpisodeListSerializer
from .serializers import AnimeSerializer, EpisodeSerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import AnimeFilter




CHUNK_SIZE = 8192



class AnimeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AnimeSerializer
    queryset = Animes.objects.all()

    # qidiruv + filter + sort
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AnimeFilter

    # ?search=...
    search_fields = ["title", "descriptions"]

    # ?ordering=created_at yoki ?ordering=-created_at
    ordering_fields = ["created_at", "release_date", "episodes", "title"]
    ordering = ["-created_at"]  # default

class AnimeEpisodeListAPIView(generics.ListAPIView):
    serializer_class = EpisodeSerializer
    permission_classes = [IsAuthenticated]  # JWT bilan kirish shart

    def get_queryset(self):
        anime_id = self.kwargs["anime_id"]
        return (
            Episode.objects
            .select_related("anime")
            .filter(anime_id=anime_id)
            .order_by("episode_number")
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

class AnimeEpisodesListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EpisodeListSerializer

    def get_queryset(self):
        anime_id = self.kwargs["anime_id"]
        # 404 agar anime yo'q bo'lsa
        get_object_or_404(Animes, pk=anime_id)

        return (
            Episode.objects
            .filter(anime_id=anime_id)
            .order_by("episode_number")
        )

class EpisodeVideoStreamView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk: int):
        episode = get_object_or_404(Episode, pk=pk)

        if not episode.video:
            raise Http404("Video mavjud emas")

        video_path = episode.video.path
        if not os.path.exists(video_path):
            raise Http404("Video fayl topilmadi")

        file_size = os.path.getsize(video_path)

        content_type, _ = mimetypes.guess_type(video_path)
        content_type = content_type or "application/octet-stream"

        range_header = request.headers.get("Range", "").strip()



       
        m = re.match(r"bytes=(\d+)-(\d*)", range_header)
        
        if m:
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else file_size - 1

            if start >= file_size or end >= file_size or end < start:
                resp = StreamingHttpResponse(status=416)
                resp["Content-Range"] = f"bytes */{file_size}"
                resp["Accept-Ranges"] = "bytes"
                return resp

            length = end - start + 1

            def iterator(path, start_pos, nbytes):
                with open(path, "rb") as f:
                    f.seek(start_pos)
                    remaining = nbytes
                    while remaining > 0:
                        chunk = f.read(min(CHUNK_SIZE, remaining))
                        if not chunk:
                            break
                        remaining -= len(chunk)
                        yield chunk

            resp = StreamingHttpResponse(
                iterator(video_path, start, length),
                status=206,
                content_type=content_type,
            )
            resp["Content-Length"] = str(length)
            resp["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        else:
            # Range yo‘q bo‘lsa, to‘liq oqim
            resp = StreamingHttpResponse(open(video_path, "rb"), content_type=content_type)
            resp["Content-Length"] = str(file_size)

        resp["Accept-Ranges"] = "bytes"
        # ixtiyoriy: cachingni o‘chirib qo‘ysang bo‘ladi
        resp["Cache-Control"] = "no-store"
        return resp




from .models import SavedAnime
from .serializers import SavedAnimeSerializer
from rest_framework import generics, status



class SavedAnimeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedAnimeSerializer

    def get_queryset(self):
        return SavedAnime.objects.select_related("anime").filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        anime_id = request.data.get("anime_id")
        if not anime_id:
            return Response({"detail": "anime_id required"}, status=status.HTTP_400_BAD_REQUEST)

        anime = get_object_or_404(Animes, pk=anime_id)
        obj, created = SavedAnime.objects.get_or_create(user=request.user, anime=anime)

        ser = self.get_serializer(obj)
        return Response(ser.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class SavedAnimeDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, anime_id: int):
        SavedAnime.objects.filter(user=request.user, anime_id=anime_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SavedAnimeToggleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, anime_id: int):
        anime = get_object_or_404(Animes, pk=anime_id)
        obj = SavedAnime.objects.filter(user=request.user, anime=anime).first()
        if obj:
            obj.delete()
            return Response({"saved": False}, status=status.HTTP_200_OK)

        SavedAnime.objects.create(user=request.user, anime=anime)
        return Response({"saved": True}, status=status.HTTP_201_CREATED)