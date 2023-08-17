import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api import db
from bson import json_util
from bson import ObjectId

# Create your views here.

mydb = db.myclient["myShop"]
mycol = mydb["users"]


def home(request):
    return HttpResponse("<h1>api is working</h1>")


@csrf_exempt
def addUser(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode("utf-8")
            body = json.loads(body_unicode)
            print(body)
            user = mycol.insert_one(body)
            return HttpResponse(user.inserted_id)
        except json.decoder.JSONDecodeError as e:
            return HttpResponse(
                f"Invalid JSON data: {e}", status=400
            )  # Return a bad request response for invalid JSON
    else:
        return HttpResponse(
            "Sorry, method doesn't exist", status=404
        )  # Return a not found response for non-POST requests


def users(request):
    users = mycol.find()
    list_curr = list(users)
    body = json_util.dumps(list_curr)
    data = json.dumps(body)
    result = json.loads(data)
    return HttpResponse(result)

    """ update and delete by user name """


@csrf_exempt
def user(request, name):
    query = {"name": name}
    if request.method == "PUT":
        try:
            body_unicode = request.body.decode("utf-8")
            body = json.loads(body_unicode)
            new_values = {"$set": body}
            mycol.update_one(query, new_values)
            user = mycol.find(query)
            list_curr = list(user)
            body = json_util.dumps(list_curr)
            result = json.dumps(body)
            js = json.loads(result)
            return HttpResponse(js)
        except json.decoder.JSONDecodeError as e:
            return HttpResponse(
                f"Invalid JSON data: {e}", status=400
            )  # Return a bad request response for invalid JSON
    if request.method == "DELETE":
        try:
            mycol.delete_one(query)
            return HttpResponse("DELETED SUCCSESSFULLY")
        except json.decoder.JSONDecodeError as e:
            return HttpResponse(
                f"Invalid JSON data: {e}", status=400
            )  # Return a bad request response for invalid JSON

    """ update and delete by user id """


"""       
@csrf_exempt
def user(request, user_id):
    try:
        object_id = ObjectId(user_id)
        query = {"_id":object_id}
        
        # UPDATE USER
        if (request.method == "PUT"):
            try:
                body_unicode = request.body.decode("utf-8")
                body = json.loads(body_unicode)
                new_values = {"$set":body}
                mycol.update_one(query, new_values)
                user = mycol.find(query)
                list_curr = list(user)
                body = json_util.dumps(list_curr)
                result = json.dumps(body)
                js = json.loads(result)
                return HttpResponse(js)
            except json.decoder.JSONDecodeError as e:
                return HttpResponse(f"Invalid JSON data: {e}", status=400)  # Return a bad request response for invalid JSON
        
        # DELETE USER
        if (request.method == "DELETE"):
        try:
            mycol.delete_one(query)
            return HttpResponse("DELETED SUCCESSFULLY")
        except json.decoder.JSONDecodeError as e:
            return HttpResponse(f"Invalid JSON data: {e}", status=400)  # Return a bad request response for invalid JSON
    except InvalidId:
        return HttpResponse("Invalid user ID", status=400)  
    
  """
