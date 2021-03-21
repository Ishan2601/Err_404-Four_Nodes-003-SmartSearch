from typing import List, Dict

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

import scipy
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np

class Utils:
    @staticmethod
    def clean_term(search_term: str, question_words : List[str]) -> str:
        """
            Cleans the search term
        """
        clean = []
        for word in word_tokenize(search_term):
            if word not in set(stopwords.words('english')):
                if word not in question_words:
                    clean.append(word)
        clean_s = ' '.join(clean)
        return clean_s

    @staticmethod
    def get_clusters(search_term: str, questions: Dict[str,List[str]]):
        """
            Gets the clusters
        """
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        query = search_term
        # Convert the corpus into a list of questions
        corpus=[]
        for value in list(questions.values()):
            corpus.extend(value)

        # Get a vector for each question (sentence) in the corpus
        corpus_embeddings = model.encode(corpus)

        # Define search queries and embed them to vectors as well
        query_embeddings = model.encode(query)

        # For each search term return 5 closest sentences
        closest_n = 5
        distances = scipy.spatial.distance.cdist([query_embeddings], corpus_embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])

        num_clusters = 10
        clustering_model = KMeans(n_clusters=num_clusters)
        clustering_model.fit(corpus_embeddings)
        cluster_assignment = clustering_model.labels_
        clusters = {}
        for i in range(10):
            clusters[i] = []
            clust_sent = np.where(cluster_assignment == i)
            for k in clust_sent[0]:
                 clusters[i].append(corpus[k])

        return clusters,corpus,results