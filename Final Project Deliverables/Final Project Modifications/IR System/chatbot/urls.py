from django.urls import path
from . import views
urlpatterns = [
    path('',views.chatbot,name='chatbot'),
    path('paraphrase',views.paraphrase,name='paraphrase')
]
