from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from graph.models import Mot, Relation, num_publis, num_auteurs
from django.core.serializers import serialize
from django.db.models import F

import pandas as pd 
from graph.ml.search_articles import SemanticSimilarity 


model = SemanticSimilarity(list(Mot.objects.all().values()), "./graph/ml/corpus_embeddings.pt")

def transform (elmt):
    elmt["parent"] = ""
    return elmt

def showArticle (resquest, id_article=1):
    
    listAuteur = num_auteurs.objects.filter(id_publi = id_article)
    if len(listAuteur)>3:
        listAuteur =listAuteur[0:5] 
    article = num_publis.objects.get(pk = id_article)
    return render(resquest, "layouts/articleDetail.html", {"article":article, "auteurs":listAuteur} )


class RequestAllTree(View):

    def get(self, request):

        str1 = "id_parent"
        getRequest1 = Mot.objects.filter(identifiant=1).values("id", name=F("motcol"))
        getRequest1 = list(getRequest1)
        getRequest1 = list(map(transform, getRequest1))

        getRequest2 = Relation.objects.all().values( parent=F("id_enfant__motcol"), name=F(str1+"__motcol"), niveau=F(str1+"__niveau"), texte=F(str1+"__resume"), id_base=F(str1+"__identifiant"))
        getRequest2 = list(getRequest2)
        

        getRequest = getRequest1 + getRequest2 
        df = pd.DataFrame(getRequest)
        return JsonResponse(getRequest, safe=False)



class RequestRelation(View):
    ### Les types de vues : 
    # https://docs.djangoproject.com/fr/3.1/ref/class-based-views/base/
    

    def get(self, request, id_word = None,  successor = None):
    
        ## Doc requetes : https://docs.djangoproject.com/fr/3.1/topics/db/queries/
        ## Exemple de requete possible    
        str1 = "id_parent"
        getRequest = Relation.objects.all().values( name=F("id_enfant__motcol"), parent=F(str1+"__motcol"), niveau=F(str1+"__niveau"), texte=F(str1+"__resume"), id_base=F(str1+"__identifiant"))
        getRequest = list(getRequest)



        if id_word != None and successor != None: 
            str1 = "id_parent"
            getRequestS = Relation.objects.filter(id_enfant=id_word, id_parent=successor).select_related("parent").values( name=F("id_enfant"), parent=F(str1), mot=F(str1+"__motcol"),niveau=F(str1+"__niveau"), id_base=F(str1+"__identifiant"))
            str1 = "id_enfant"
            getRequestP = Relation.objects.filter(id_parent=id_word, id_enfant=successor).select_related('enfant').values( name=F("id_parent") , parent=F(str1), mot=F(str1+"__motcol"), niveau=F(str1+"__niveau"), id_base=F(str1+"__identifiant"))
            getRequest = list(getRequestP) + list(getRequestS)

        elif id_word != None:
            str1 = "id_parent"
            getRequestS = Relation.objects.filter(id_enfant=id_word).values( name=F("id_enfant__motcol"), parent=F(str1+"__motcol"), id_mot = F(str1) , niveau=F(str1+"__niveau"), id_base=F(str1+"__identifiant"))
            # str1 = "id_enfant"
            # getRequestP = Relation.objects.filter(id_parent=id_word).select_related('enfant').values(name=F("id_parent") , parent=F(str1), mot=F(str1+"__motcol"), niveau=F(str1+"__niveau"), id_base=F(str1+"__identifiant"))
            getRequest = list(getRequestS)# + list(getRequestP)

        
        else:
            str1 = "id_parent"
            getRequest = Relation.objects.all().values( name=F("id_enfant__motcol"), parent=F(str1+"__motcol"), niveau=F(str1+"__niveau"), texte=F(str1+"__resume"), id_base=F(str1+"__identifiant"))
            getRequest = list(getRequest)
            # str1 = "id_enfant"
            # getRequestP = Relation.objects.all().select_related('enfant').values(name=F("id_parent") , enfant=F(str1), mot=F(str1+"__motcol"), niveau=F(str1+"__niveau"), id_base=F(str1+"__identifiant"))
            # getRequest = list(getRequestP) + list(getRequestS)
        
        return JsonResponse(getRequest, safe=False)


class Requestmot(View):
    ### Les types de vues : 
    # https://docs.djangoproject.com/fr/3.1/ref/class-based-views/base/
    

    def get(self, request, id_mot=None, article=None):# pk=None, level=None, word=None ):
        ## Doc requetes : https://docs.djangoproject.com/fr/3.1/topics/db/queries/
        ## Exemple de requete possible
        
        getRequest = Mot.objects.filter(id__in = model.search_n_articles(id_mot)).values("id", name=F("motcol"))
        getRequest = list(getRequest)
        getRequest1 = Mot.objects.values_list("id", "motcol", "resume").get(id=id_mot)
        getRequest = list(getRequest1) + getRequest 

        return JsonResponse(getRequest, safe=False)


