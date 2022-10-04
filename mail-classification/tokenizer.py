import spacy
from collections import Counter

mail_stop_words = {"subject", "from", "to", "cc", "|"}
part_of_speeches = {"ADJ", "ADV", "NOUN", "PROPN", "VERB"}

class Tokenizer:

    def __init__(self, stop_words, part_of_speeches):
        self._nlp_model = spacy.load("en_core_web_sm")
        self._stop_words = stop_words
        self._nlp_model.Defaults.stop_words |= stop_words
        self._part_of_speeches = part_of_speeches

    def _legal_token(self, token):
        return not token.is_stop and \
               not token.is_punct and \
               token.text not in self._stop_words and \
               token.pos_ in self._part_of_speeches

    def tokens_count(self, text):
        doc = self._nlp_model(text)
        tokens = [token.text
                    for token in doc
                    if self._legal_token(token)]

        return Counter(tokens)

    @staticmethod
    def default_tokenizer():
        return Tokenizer(mail_stop_words, part_of_speeches)