import math


class Model:
    def __init__(self, model_dict):
        data_count = float(sum(model_dict["classes"].values()))
        self._classes_freq = {class_name: count / data_count for class_name, count in model_dict["classes"].items()}

        self._words_freq = {}
        for word, classes_dict in model_dict["data"].items():
            words_count = sum(token_class["wc"] for token_class in classes_dict.values() if token_class)
            word_in_docs_count = sum(token_class["dc"] for token_class in classes_dict.values() if token_class)

            for class_name, token_class in classes_dict.items():
                res = (data_count - token_class["dc"]) / (float(word_in_docs_count - token_class["dc"]) + 0.1)
                idf = math.log2(res)
                freq = idf
                if word in self._words_freq:
                    self._words_freq[word].update({class_name: freq})
                else:
                    self._words_freq[word] = {class_name: freq}

        classes_count = len(model_dict["classes"])
        self._outer_words_freq = {class_name: 1.0 / classes_count for class_name in model_dict["classes"].keys()}

    def classes(self):
        return list(self._classes_freq.keys())

    def class_freq(self, class_name):
        return self._classes_freq[class_name]

    def classes_freq(self):
        return dict(self._classes_freq)

    def word_freq(self, word):
        if word not in self._words_freq:
            return self._classes_freq

        word_freq = {class_name: word_freq for class_name, word_freq in self._words_freq[word].items()}
        for class_name in self._classes_freq.keys():
            if class_name not in word_freq:
                word_freq[class_name] = self._classes_freq[class_name]

        return word_freq