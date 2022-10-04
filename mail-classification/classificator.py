class NativeBayesClassificator:
    def __init__(self, trained_model):
        self._trained_model = trained_model

    def classify(self, words):
        classes_probability = self._trained_model.classes_freq()

        for word in words:
            word_freq = self._trained_model.word_freq(word)

            for class_name, probability in classes_probability.items():
                classes_probability[class_name] = probability * word_freq[class_name]

        return classes_probability