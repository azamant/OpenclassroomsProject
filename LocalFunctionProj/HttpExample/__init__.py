import logging
import pickle
import pandas as pd
from collections import defaultdict

import azure.functions as func
import subprocess

class AzureFilter():
    def __init__(self, articles, predictions):
        self.articles = articles
        self.predictions = predictions
    
    def get_top_n(self, n=10):

        # First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in self.predictions:
            top_n[uid].append((iid, est))

        # Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]
        return top_n
    
    def findRecom(self,dic, userId):
        res = []
        query = dic[userId]
        for uid, user_ratings in query:
            res.append(uid)
        return res
    
    def GetUserRecom(self,userId):
        """ Fonction qui renvoi 5 articles au hasard parmis les catégories retenues"""
        top_n = self.get_top_n(n=5)
        res = self.findRecom(top_n,userId)
        temp = []

        for id in res:
            df = self.articles[self.articles['category_id']==id]
            temp.append(df)

        retour = pd.concat(temp, axis=0, ignore_index=True)
        retour = retour.sample(n=5)
        return retour

ARTICLE_PATH = "../dependencies/articles_metadata.csv"
PEDICT_PATH = "../dependencies/predictions.pkl"

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        article_subpath= "/".join([str(context.function_directory), ARTICLE_PATH])
        articles = pd.read_csv(article_subpath)
        predic_subpath= "/".join([str(context.function_directory), PEDICT_PATH])
        pickled_predic = pickle.load(open(predic_subpath, 'rb'))
        CollabFilter = AzureFilter(articles, pickled_predic)
        liste = CollabFilter.GetUserRecom(int(name))
        return liste.to_json(orient='table')
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. rentrez un identifiant utilisateur.",
             status_code=200
        )
