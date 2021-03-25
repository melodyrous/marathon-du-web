function takeData(url){
    // https://github.com/d3/d3-request/blob/master/README.md#json
    
    var data = data
    d3.request(url, function(error, response) {
        data = response
    });
}


/**
 * Liste des requetes possibles pour le graph : 
 * 
 * 
 * ######## Niveau relation, trois niveau :
 * 
 * resquestRelationAll/idword=1                  => Le premier niveau récupérer tous les mots associé à idword (identifiant du mot en question qui est égale à 1 ici)                        idword=1 puis /rel=-1/succ=-1
 * 
 * resquestRelationNiveau/idword=1/rel=apa       => Le second niveau récupérer tous les mots associé à idword = 1 et un type demandé ici apa (identifiant du mot en question)      idword=1/rel=mots associé puis /succ=-1
 * 
 * resquestRelationSuccessor/idword=1/succ=3     => Le troisième niveau récupérer tous les mots associé à idword = 1 et l'id d'un successeur précis ici 3                             idword=1/rel=mots associé/succ=3
 * 
 * 
 * ######## Niveau mots, trois niveaux :
 * 
 * resquestMotID/id=1/                           => Recupère le mots dont l'id est 1
 * 
 * graph/resquestMotSTR/mot=psy/                 => Recupère le/les mots nommée psy
 * 
 * resquestMotLVL/niveau=d/exclude=1/            => Recupère les mots du niveau d uniquement
 *  
 * resquestMotLVL/niveau=d/exclude=0/            => Recupère les mots de tous les niveaux sauf d
 */