import json
from django.http import HttpResponse
from django.core import serializers
from myapp.models import User

def get_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        json_data = serializers.serialize('json', [user])
        return HttpResponse(json_data, content_type='application/json')
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)
