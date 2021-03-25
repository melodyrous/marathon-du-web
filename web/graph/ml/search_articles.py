import torch
import pandas as pd
from sentence_transformers import SentenceTransformer, util


import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup

import html 
import re
import numpy as np

class Data_utils():

    def __init__(self):

        self.original_dataframe = self.prepare_original_dataframe()

    def get_all_publis_from_database(self):
        db_df = pd.read_csv("mot.csv", sep=";",encoding="utf8", names =["idmot","motcol","niveau","identifiant","resume"])
        return db_df

    def prepare_original_dataframe(self):
        """ Prepare the original dataframe from full corpus """
        def cleanhtml(raw_html):
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', raw_html)
            return html.unescape(cleantext)

        df_publis = self.get_all_publis_from_database()
        df_publis["motcol"] = df_publis.motcol.apply(lambda x: cleanhtml(BeautifulSoup(x).text))
        df_publis["resume"] = df_publis.resume.apply(lambda x: cleanhtml(BeautifulSoup(x).text) if x is not np.NaN else x)
        return df_publis



class SemanticSimilarity():

    def __init__(self):
        #self.corpus_embeddings = torch.load("./notebooks/corpus_embeddings.pt")
        self.corpus_embeddings = torch.load("./corpus_embeddings.pt")
        self.data_utils = Data_utils()
        self.data_corpus = self.prepare_original_dataframe()
        self.model = SentenceTransformer('allenai-specter')



    def search_n_articles(self,id_article):
        """ Get the n most similar articles contained in the database compute from cosine similarity 
        distance between tensors.
        Parameters:
        -----------
        id_article: int, the id of the original article  
        n: int, the number of articles returned from the search request
        Returns: List(int), list of ids of the most semantically similar articles
        """
        #TODO prétraiter le texte importé
        df_publis = self.data_utils.original_dataframe
        paper = df_publis[df_publis.idmot == id_article]
#        print(paper)
        text = paper.motcol +" "+ paper.resume

        query_embedding = self.model.encode(text.values[0], convert_to_tensor=True)

        search_articles = util.semantic_search(query_embedding, self.corpus_embeddings)[0] 
        matchs = []
        for hit in search_articles:
            related_paper = self.data_corpus.iloc[hit['corpus_id'],:]
            titre_selected = self.data_utils.original_dataframe.motcol == related_paper['motcol']
            if self.data_utils.original_dataframe[titre_selected].resume.values[0] != ";":
                matchs.append(self.data_utils.original_dataframe[titre_selected].idmot.values[0])
            
            
        
        return matchs



    def prepare_original_dataframe(self):
        """Prepare the dataframe """
        df_publis = self.data_utils.original_dataframe
        df = df_publis.loc[:,["motcol","resume","idmot"]].dropna()
        return df