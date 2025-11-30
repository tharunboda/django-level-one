from django.http import Jsonresponse
from django.http import HttpResponse

class movieReviewMiddleWare:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if request.path=="/movie/" and request.method=="POST":
            incoming_data=request.POST
            print(incoming_data)
            # print("incoming data",incoming_data)
            if not incoming_data.get("rating"):
                return Jsonresponse({"error":"rating is requred"},status=400)
            elif float(incoming_data.get("rating"))<0  or float(incoming_data.get("rating"))>10:
                return Jsonresponse({"error":"rating should be between 0 to 10"},status=400)
            elif not incoming_data.get("budget"):
                return Jsonresponse({"error":"budget is requred"},status=400)
            elif not incoming_data.get("movie_name"):
                return Jsonresponse({"error":"movie_name is requred"},status=400)
            elif not incoming_data.get("release_date"):
                return Jsonresponse({"error":"release_date is requred"},status=400)
        return self.get_response(request)