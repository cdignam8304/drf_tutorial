from django.urls import path, include
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

# API endpoints
urlpatterns = [
   path("", views.api_root), # tut5
   # path("snippets/", views.snippet_list,), # tut1&2
   # path("snippets/", views.SnippetList.as_view(),), # tut3
   # path("snippets/", views.SnippetList_Mx.as_view(),), # tut3
   # path("snippets/", views.SnippetList_GCBV.as_view(),), # tut3
   path("snippets/", views.SnippetList_GCBV.as_view(), name="snippet-list"), # tut5
   # path("snippet/<int:pk>/", views.snippet_detail,), # tut1&2
   # path("snippet/<int:pk>/", views.SnippetDetail.as_view(),), # tut3 
   # path("snippet/<int:pk>/", views.SnippetDetail_Mx.as_view(),), # tut3
   # path("snippet/<int:pk>/", views.SnippetDetail_GCBV.as_view(),), # tut3
   path("snippet/<int:pk>/", views.SnippetDetail_GCBV.as_view(), name="snippet-detail"), # tut5
   # path("snippets/<int:pk>/highlight/", views.SnippetHighlight.as_view()), # tut5
   path("snippets/<int:pk>/highlight/", views.SnippetHighlight.as_view(), name="snippet-highlight"), # tut5 v2
   # path("users/", views.UserList.as_view(),), # tut4
   path("users/", views.UserList.as_view(), name="user-list"), # tut5
   # path("user/<int:pk>/", views.UserDetail.as_view(),), # tut4
   path("user/<int:pk>/", views.UserDetail.as_view(), name="user-detail"), # tut5
]

# Allows a url to contain a suffix like .json or .api to specify the response type for a GET request or
# to specify data format being sent on a POST/PUT/DELETE request.
urlpatterns = format_suffix_patterns(urlpatterns) # tut2

# tut4
# include login and logout views for the browsable API
urlpatterns += [
   path("api-auth/", include("rest_framework.urls")),
]