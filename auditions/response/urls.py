
from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.index,name="index"),
   path('get_question/',views.get_question,name="get-question"),
   path('get_question_image/',views.get_question,name="get-question_image"), 
]
