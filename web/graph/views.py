from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from graph.models import Mot, Relation, num_publis, num_auteurs
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
    

    def get(self, request, id_word = None,  successor = None):
    
        ## Doc requetes : https://docs.djangoproject.com/fr/3.1/topics/db/queries/
        ## Exemple de requete possible    
        
        print( Relation.objects.all().values())
        if id_word != None and successor != None: 
            str1 = "id_parent"
            getRequestS = Relation.objects.filter(id_enfant=id_word, id_parent=successor).select_related("parent").values( parent=F("id_enfant"), enfant=F(str1), mot=F(str1+"__motcol"),niveau=F(str1+"__niveau"), id_base=F(str1+"__identifiant"))
            str1 = "id_enfant"
            getRequestP = Relation.objects.filter(id_parent=id_word, id_enfant=successor).select_related('enfant').values(parent=F("id_parent") , enfant=F(str1), mot=F(str1+"__motcol"), niveau=F(str1+"__niveau"), id_base=F(str1+"__identifiant"))
            getRequest = list(getRequestP) + list(getRequestS)

        elif id_word != None:
            str1 = "id_parent"
            getRequestS = Relation.objects.filter(id_enfant=id_word).select_related("parent").values( parent=F("id_enfant"), enfant=F(str1), mot=F(str1+"__motcol"),niveau=F(str1+"__niveau"), id_base=F(str1+"__identifiant"))
            str1 = "id_enfant"
            getRequestP = Relation.objects.filter(id_parent=id_word).select_related('enfant').values(parent=F("id_parent") , enfant=F(str1), mot=F(str1+"__motcol"), niveau=F(str1+"__niveau"), id_base=F(str1+"__identifiant"))
            getRequest = list(getRequestP) + list(getRequestS)
        
        else:
            getRequest = list(Relation.objects.all().values())
        
        return JsonResponse(getRequest, safe=False)


class Requestmot(View):
    ### Les types de vues : 
    # https://docs.djangoproject.com/fr/3.1/ref/class-based-views/base/
    

    def get(self, request, id_mot=None, mot= None, niveau=None, exclude=0, cat=None):# pk=None, level=None, word=None ):
        print(id_mot, mot, niveau, exclude)
        ## Doc requetes : https://docs.djangoproject.com/fr/3.1/topics/db/queries/
        ## Exemple de requete possible
        if not id_mot == None:
            getRequest = Mot.objects.filter(id=id_mot)
        elif not mot == None:
            getRequest = Mot.objects.filter(motcol=mot)
        elif not niveau == None:
            if not exclude == 0 :
                getRequest = Mot.objects.filter(identifiant=niveau).values("id", name=F("motcol") )
            else:
                getRequest = Mot.objects.exclude(identifiant=niveau)
        
        getRequest = list(getRequest)
        
        return JsonResponse(getRequest, safe=False)


