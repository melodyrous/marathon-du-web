from django.db import models

# Create your models here.
## https://www.youtube.com/watch?v=bHnT1apz8u8&list=PL5smYbP6KikObRFD1C0Kh9wrIhWfbSvnP&index=3

################################ Issue de notre base de donnée créer ################################


class Mots(models.Model):
    ## Doc pour la création des models : https://docs.djangoproject.com/fr/3.1/ref/models/fields/
    mots = models.TextField()
    niveau = models.CharField(max_length=40)
    id_in_base = models.IntegerField(blank=True)
    class Meta:
        db_table="mots"


class Relation(models.Model):
    id_predecesseur = models.ForeignKey(Mots, on_delete=models.CASCADE, related_name='predecesseur')
    id_sucesseur = models.ForeignKey(Mots, on_delete=models.CASCADE, related_name='sucesseur')
    # type_relation = models.CharField(max_length=40)
    class Meta:
        db_table="relation"


################################ Issue la base de donnée Numerav ################################

class num_publis(models.Model):
    id_revue = models.IntegerField()
    id_numero = models.IntegerField()
    type = models.IntegerField()
    titre = models.TextField()
    soustitre = models.TextField()
    position = models.IntegerField()
    resume = models.TextField()
    article = models.TextField()
    id_ecriture_parent = models.IntegerField()
    slug = models.CharField(max_length=40)
    date_publication = models.IntegerField()
    valid = models.IntegerField() 
    class Meta:
        db_table="num_publis"

class num_auteurs(models.Model):
    id_user = models.CharField(max_length=40)
    id_publi = models.ForeignKey(num_publis, on_delete=models.CASCADE)
    position = models.IntegerField()
    valid = models.IntegerField() 

    class Meta:
        db_table="num_auteurs"

