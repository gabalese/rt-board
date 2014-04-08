import json
import datetime
import time

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render_to_response

from haas.models import *


def ping(request):
    output = {"status": "OK", "timestamp": datetime.datetime.now().strftime("%s")}
    return HttpResponse(json.JSONEncoder().encode(output))


def main_view(request):
    return render_to_response('index.html')


def submit_message(request):
    if request.method != "POST":
        return StreamingHttpResponse("NOPE!", status=405)
    else:
        if request.POST.get("author", False):
            try:
                author = Author.objects.get(name__exact=request.POST["author"])
            except Author.DoesNotExist:
                author = Author()
                author.name = request.POST["author"]
                author.save()
        else:
            try:
                author = Author.objects.get(name__exact="Anonymous")
            except Author.DoesNotExist:
                author = Author()
                author.name = "Anonymous"
                author.save()
        message = Message()
        message.title = request.POST["title"]
        message.text = request.POST["text"]
        message.author = author
        try:
            message.save()
        except Exception as e:
            print e
        return StreamingHttpResponse("OK", status=200)


def show_single_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return HttpResponse("No message found. Having a good day, don't ya?", status=404, reason="Not found.")
    return render_to_response('single.html', {"message": message})


def updates_show(request, last_id):
    """
    Django implementation of a "long polling" endpoint.
    """
    for _ in xrange(20):
        messages = Message.objects.filter(id__gt=last_id)
        count = messages.count()
        if count == 0:
            time.sleep(1)
            continue
        return HttpResponse(json.dumps(messages))
