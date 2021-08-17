from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


# THIS API WILL SUPPORT VIEWING A LIST OF SNIPPETS OR ADDING A NEW SNIPPET

# @csrf_exempt # tut1
@api_view(["GET", "POST"]) # tut2
# def snippet_list(request): # tut1
def snippet_list(request, format=None): # tut2
    """
    List all code snippets or create a new snippet.
    """
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        # return JsonResponse(serializer.data, safe=False) # tut1
        return Response(serializer.data) # tut2

    elif request.method == "POST":
        # data = JSONParser().parse(request) # tut1
        # serializer = SnippetSerializer(data=data) # tut1
        serializer = SnippetSerializer(data=request.data) # tut2
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data, status=201) # tut1
            return Response(serializer.data, status=status.HTTP_201_CREATED) # tut2
        # return JsonResponse(serializer.errors, status=400) # tut1
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST) # tut2


# @csrf_exempt # tut1
@api_view(["GET", "PUT", "DELETE"]) # tut2
# def snippet_detail(request, pk): # tut1
def snippet_detail(request, pk, format=None): # tut2
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    # except: # tut1
        # return HttpResponse(status=404) # tut1
    except Snippet.DoesNotExist: # tut2
        return Response(status=status.HTTP_404_NOT_FOUND) # tut2
    
    if request.method == "GET":
        serializer = SnippetSerializer(snippet)
        # return JsonResponse(serializer.data) # tut1
        return Response(serializer.data) # tut2
    
    elif request.method == "PUT":
        # data = JSONParser().parse(request) # tut1
        # serializer = SnippetSerializer(snippet, data=data) # tut1
        serializer = SnippetSerializer(snippet, data=request.data) # tut2
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data) # tut1
            return Response(serializer.data) # tut2
        # return JsonResponse(serializer.errors, status=400) # tut1
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # tut2
    
    elif request.method == "DELETE":
        snippet.delete()
        # return HttpResponse(status=204) # tut1
        return Response(status=status.HTTP_204_NO_CONTENT) # tut2
