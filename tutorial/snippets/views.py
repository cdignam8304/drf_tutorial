from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly # tut4


# THIS API WILL SUPPORT VIEWING A LIST OF SNIPPETS OR ADDING A NEW SNIPPET

# FUNCTION-BASED VIEWS (Tutorials 1 & 2)
# --------------------------------------

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


# CLASS-BASED VIEWS (Tutorial 3+)
# -------------------------------

# 1. Without Mixins
# -----------------

class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
    Retrieve, Update or Delete a snippet instance.
    """
    
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk=pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk=pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk=pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 2. With Mixins (simpler code) - PROVIDES FORM IN WEB API VIEW FOR CREATE AND UPDATE
# -----------------------------------------------------------------------------------

class SnippetList_Mx(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView): # GenericAPIView provides core functionality

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs) # bind get request to the ListModelMixin
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs) # bind post request to the CreateModelMixin


class SnippetDetail_Mx(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView): # GenericAPIView provides core functionality

    queryset = Snippet.objects.all() # suprising! Is this pulling all instances from database?
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# 3. Generic Class Based Views (even simpler code!)
# -------------------------------------------------

class SnippetList_GCBV(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # tut4

    # tut4
    # We are overriding the perform_create method in order to capture the username that is
    # performing request, which we use as the owner of the snippet.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail_GCBV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly, # only snippet owner should be allowed to edit it.
        ] # tut4


class UserList(generics.ListAPIView): # this provides a read-only list
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView): # this provides a read-only view of single user
    querset = User.objects.all()
    serializer_class = UserSerializer