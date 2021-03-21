from typing import List

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

class Utils:
    @staticmethod
    def clean_term(self, search_term: str, question_words : List[str]) -> str:
        """
            Cleans the search term
        """
        clean = []
        for word in word_tokenize(search_term):
            if word not in set(stopwords.words('english')):
                if word not in self.question_words:
                    clean.append(word)
        clean_s = ' '.join(clean)
        return clean_s