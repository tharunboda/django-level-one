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
    if request.method=="GET":
        movie_info=Movie_details.objects.all()
        movie_list=[]
        rating_filter=request.GET.get("rating")
        min_bud_filter=request.GET.get("min_budget")
        max_bud_filter=request.GET.get("max_budget")
        if rating_filter:
             movie_info = movie_info.filter(rating__gte=float(rating_filter))
            
        for movie in movie_info:
            if min_bud_filter or max_bud_filter:
                budget_str=movie.budget.lower().replace("cr","")
                budget_value=float(budget_str)
                if min_bud_filter and budget_value < float(min_bud_filter):
                    continue
                if max_bud_filter and budget_value > float(max_bud_filter):
                    continue

            movie_list.append({
                "movie_name":movie.movie_name,
                "release_date":movie.release_date,
                "budget":movie.budget,
                "rating":movie.rating
            })
        if len(movie_list)==0:
            return JsonResponse({"status":"success","message":"No movie found in a criteria"},status=200)
        return JsonResponse({"status":"success","data":movie_list},status=200)
    
    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id")
        existing_movie=Movie_details.objects.get(id=ref_id)
        if data.get("movie_name"):
            new_movie_name=data.get("movie_name")
            existing_movie.movie_name=new_movie_name
            existing_movie.save()
            
        elif data.get("release_date"):
            new_release_date=data.get("release_date")
            existing_movie.release_date=new_release_date
            existing_movie.save()
        elif data.get("budget"):
            new_budget=data.get("budget")
            existing_movie.budget=new_budget
            existing_movie.save()
        elif data.get("rating"):
            new_rating=data.get("rating")
            existing_movie.rating=new_rating
            existing_movie.save()
        return JsonResponse({"status":"success","message":"movie record updated successfully","data":data},status=200)
    elif request.method=="DELETE":
        data=request.GET.get("id")
        ref_id=data
        existing_movie=Movie_details.objects.get(id=ref_id)
        existing_movie.delete()
        return JsonResponse({"status":"success","message":"movie recored deleted successfully"},status=200)

    elif request.method=="POST":
        data=json.loads(request.body) #whenever we send data in json format we have to use this
        # data=request.POST #when we send data in form format we have to use this
        # print(data.get("movie_name"),"hello")
        # rating=int(data.get("rating"))
        # star_rating="*"*rating
        # data["rating"]=star_rating
        movie=Movie_details.objects.create(movie_name=data.get("movie_name"),release_date=data.get("release_date"),budget=data.get("budget"),rating=data.get("rating"))
        return JsonResponse({"status":"success","message":"movie record inserted successfully","data":data},status=200)
    return JsonResponse({"error":"error occured"},status=400)
    
