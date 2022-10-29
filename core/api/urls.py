from django.urls import path
from core.api.endpoints import *

urlpatterns = [
    path('labels/', LabelListCreate.as_view()),
    path('labels/<int:pk>/', label_detail),
    path('notes/', NoteList.as_view()),
    path('notes/<int:pk>/', NoteDetail.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]
