
from django.urls import path

from . import views # import views so we can use them in urls.

urlpatterns = [
    
    path('idarticle=<int:id_article>', views.showArticle, name="article"),
    
    ## Doc pour comprendre le url : https://docs.djangoproject.com/fr/3.1/topics/http/urls/

    #### Get relation ####
    # exemple requete : http://127.0.0.1:8000/graph/resquestRelation/idword=1/rel=apa/succ=3
    # http://127.0.0.1:8000/graph/resquestRelation/idword=1/rel=-1/succ=1

    ### resquestRelationAll/idword=1
    path('resquestRelationAll/idword=<int:id_word>', views.RequestRelation.as_view()),
    
    # ### resquestRelationNiveau/idword=1/rel=apa
    # path('resquestRelationNiveau/idword=<int:id_word>/rel=<str:type_relation>', views.RequestRelation.as_view()),
    
    ### resquestRelationSuccessor/idword=1/succ=3 
    path('resquestRelationSuccessor/idword=<int:id_word>/succ=<int:successor>', views.RequestRelation.as_view()),

    #### Get mot ####

    ### resquestMotID/id=1/
    path('resquestMotID/id=<int:id_mots>/', views.RequestMots.as_view()),
    
    ### graph/resquestMotSTR/mot=psy/
    path('resquestMotSTR/mot=<str:mots>/', views.RequestMots.as_view()),
    
    ### resquestMotLVL/niveau=d/exclude=0/
    ### resquestMotLVL/niveau=d/exclude=1/
    path('resquestMotLVL/niveau=<str:niveau>/exclude=<int:exclude>/', views.RequestMots.as_view()),
    
    #### Get article ####

    path('presentationArticle/<int:id_article>/', views.showArticle, name="showArticle")
    #path('allWord', views.RequestMots.as_view(), name='allWord'),
]