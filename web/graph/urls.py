
from django.urls import path

from . import views # import views so we can use them in urls.

urlpatterns = [
    
    path('idarticle=<int:id_article>', views.showArticle, name="article"),
    
    ## Doc pour comprendre le url : https://docs.djangoproject.com/fr/3.1/topics/http/urls/

    #### Get relation ####
    # exemple requete : http://127.0.0.1:8000/graph/resquestRelation/idword=1/rel=apa/succ=3
    # http://127.0.0.1:8000/graph/resquestRelation/idword=1/rel=-1/succ=1

    ### resquestRelationAll/
    path('resquestTree/', views.RequestAllTree.as_view()),
    
    ### resquestRelationSuccessor/idword=1/succ=3
    path('resquestRelation/idword=<int:id_word>', views.RequestRelation.as_view()),
    
    ### resquestRelationSuccessor/idword=1/succ=3 
    path('resquestRelation/idword=<int:id_word>/succ=<int:successor>', views.RequestRelation.as_view()),

    #### Get mot ####

    ### resquestMotID/id=1/
    path('resquestMotID/id=<int:id_mot>/', views.Requestmot.as_view()),
    path('resquestMot/id=<int:id_mot>/<str:article>', views.Requestmot.as_view()),
     path('resquestMot/id=<int:id_mot>', views.Requestmot.as_view()),
    
   
      ### resquestMotLVL/niveau=d/exclude=1/
    path('resquestMotLVL/niveau=<int:niveau>/', views.Requestmot.as_view()),
    

]