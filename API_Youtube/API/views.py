from django.shortcuts import render
from django.http import HttpResponse

from .Test_Youtube_api import getnewposts
from .models import Videos
from .serializers import VideosSerializer

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.views.generic import TemplateView
from django.http import JsonResponse

# Create your views here.

class RunFetchCommand(TemplateView):
    template_name = 'posts/main.html'
    
# def post_json(request):
#     data = list(Videos.objects.values())
#     return JsonResponse(data, safe=False)

def fetch_new_posts(request):
    try:
        getnewposts()
        return HttpResponse("New videos are being fetched! Check the python console for detailed logs.")
    except:
        return HttpResponse("Some error encountered")

class VideoList(generics.ListAPIView):
    queryset = Videos.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
   
    # Adding the search and filter fields
    search_fields = ['title']
    filter_fields = ['channelTitle']

    # For sorting the videos' data in reverse chronological order by default
    ordering = ['-publishingDateTime']
    serializer_class = VideosSerializer
    pagination_class = PageNumberPagination