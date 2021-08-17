from snippets.views import snippet_list
from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
   path("snippets/", views.snippet_list,),
   path("snippet/<int:pk>/", views.snippet_detail,), 
]

# Allows a url to contain a suffix like .json or .api to specify the response type for a GET request or
# to specify data format being sent on a POST/PUT/DELETE request.
urlpatterns = format_suffix_patterns(urlpatterns) # tut2