from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import JsonResponse
from review.models import Movie_details
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def basic(request):
    return HttpResponse("hello world")

@csrf_exempt
def movie_info(request):
    movie=request.GET.get("movie")
    date=request.GET.get("date")
    return JsonResponse({"status":"succes","result":{"movie_name":movie,"release_date":date}},status=200)


@csrf_exempt
def movies(request):
    if request.method=="POST":
        # data=json.loads(request.body) #whenever we send data in json format we have to use this
        data=request.POST #when we send data in form format we have to use this
        print(data.get("movie_name"),"hello")
        # rating=int(data.get("rating"))
        # star_rating="*"*rating
        # data["rating"]=star_rating
        movie=Movie_details.objects.create(movie_name=data.get("movie_name"),release_date=data.get("release_date"),budget=data.get("budget"),rating=data.get("rating"))
        return JsonResponse({"status":"success","message":"movie record inserted successfully","data":data},status=200)
    return JsonResponse({"error":"error occured"},status=400)
