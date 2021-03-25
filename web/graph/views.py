from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from graph.models import Mots, Relation, num_publis, num_auteurs
from django.core.serializers import serialize
from django.db.models import F

def showArticle (resquest, id_article=1):
    
    listAuteur = num_auteurs.objects.filter(id_publi = id_article)
    if len(listAuteur)>3:
        listAuteur =listAuteur[0:5] 
    article = num_publis.objects.get(pk = id_article)
    return render(resquest, "layouts/articleDetail.html", {"article":article, "auteurs":listAuteur} )


class RequestRelation(View):
    ### Les types de vues : 
    # https://docs.djangoproject.com/fr/3.1/ref/class-based-views/base/
    

    def get(self, request, id_word = None,  successor = None, type_relation = None,):
    
        ## Doc requetes : https://docs.djangoproject.com/fr/3.1/topics/db/queries/
        ## Exemple de requete possible    

        if id_word != None and successor != None: 
            str1 = "id_predecesseur"
            getRequestS = Relation.objects.filter(id_sucesseur=id_word, id_predecesseur=successor).select_related("predecesseur").values('type_relation', predecesseur=F("id_sucesseur"), sucesseur=F(str1), mot=F(str1+"__mots"),niveau=F(str1+"__niveau"), id_base=F(str1+"__id_in_base"))
            str1 = "id_sucesseur"
            getRequestP = Relation.objects.filter(id_predecesseur=id_word, id_sucesseur=successor).select_related('sucesseur').values('type_relation',predecesseur=F("id_predecesseur") , sucesseur=F(str1), mot=F(str1+"__mots"), niveau=F(str1+"__niveau"), id_base=F(str1+"__id_in_base"))
            
            getRequest = list(getRequestP) + list(getRequestS)

        # elif type_relation != None and id_word != None:
        #     str1 = "id_predecesseur"
        #     getRequestS = Relation.objects.filter(id_sucesseur=id_word, type_relation=type_relation).select_related("predecesseur").values('type_relation', predecesseur=F("id_sucesseur"), sucesseur=F(str1), mot=F(str1+"__mots"),niveau=F(str1+"__niveau"), id_base=F(str1+"__id_in_base"))
        #     str1 = "id_sucesseur"
        #     getRequestP = Relation.objects.filter(id_predecesseur=id_word, type_relation=type_relation).select_related('sucesseur').values('type_relation',predecesseur=F("id_predecesseur") , sucesseur=F(str1), mot=F(str1+"__mots"), niveau=F(str1+"__niveau"), id_base=F(str1+"__id_in_base"))
            
        #     getRequest = list(getRequestP) + list(getRequestS)
        
        elif id_word != None:
            print("lvl 1")
            str1 = "id_predecesseur"
            getRequestS = Relation.objects.filter(id_sucesseur=id_word).select_related("predecesseur").values('type_relation', predecesseur=F("id_sucesseur"), sucesseur=F(str1), mot=F(str1+"__mots"),niveau=F(str1+"__niveau"), id_base=F(str1+"__id_in_base"))
            str1 = "id_sucesseur"
            getRequestP = Relation.objects.filter(id_predecesseur=id_word).select_related('sucesseur').values('type_relation',predecesseur=F("id_predecesseur") , sucesseur=F(str1), mot=F(str1+"__mots"), niveau=F(str1+"__niveau"), id_base=F(str1+"__id_in_base"))
            getRequest = list(getRequestP) + list(getRequestS)
        
        else:
            getRequest = []
        
        return JsonResponse(getRequest, safe=False)


class RequestMots(View):
    ### Les types de vues : 
    # https://docs.djangoproject.com/fr/3.1/ref/class-based-views/base/
    

    def get(self, request, id_mots=None, mots= None, niveau=None, exclude=0):# pk=None, level=None, word=None ):
        print(id_mots, mots, niveau, exclude)
        ## Doc requetes : https://docs.djangoproject.com/fr/3.1/topics/db/queries/
        ## Exemple de requete possible
        if not id_mots == None:
            getRequest = Mots.objects.filter(pk=id_mots)
        elif not mots == None:
            getRequest = Mots.objects.filter(mots=mots)
        elif not niveau == None:
            if not exclude == 0 :
                getRequest = Mots.objects.filter(niveau=niveau)
            else:
                getRequest = Mots.objects.exclude(niveau=niveau)
        
        getRequest = list(getRequest.values())
        
        return JsonResponse(getRequest, safe=False)


