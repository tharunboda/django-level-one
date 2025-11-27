from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.

def basic(request):
    return HttpResponse("hello world")


def movie_info(request):
    movie=request.GET.get("movie")
    date=request.GET.get("date")
    return JsonResponse({"status":"succes","result":{"movie_name":movie,"release_date":date}},status=200)

