import spacy

common_words = {"apple"}

nlp = spacy.load("en_core_web_sm")
nlp.Defaults.stop_words |= common_words

doc = nlp("Apple: is, njd dstq buy BUY U.K. STARTUP startup for $1 billion!")
for token in doc:
    if not token.is_punct and not token.is_stop:
        print(token, token.lemma, token.lemma_)
