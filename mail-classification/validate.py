import json
import os.path
import sys
from model import Model
from tokenizer import Tokenizer
from classificator import NativeBayesClassificator

import operator

def max_value_key(dict):
    return max(dict.items(), key=operator.itemgetter(1))[0]

if __name__ == "__main__":
    valid_dir_name = sys.argv[1]
    file_name = sys.argv[2]

    with open(file_name, 'r') as model_file:
        trained_model = Model(json.load(model_file))

    classificator = NativeBayesClassificator(trained_model)
    with open(os.path.join(valid_dir_name, 'valid_data_list.txt'), 'r') as valid_data_file:
        file_names = valid_data_file.read().split()

    class_name = os.path.basename(valid_dir_name)
    print(class_name)
    tokenizer = Tokenizer.default_tokenizer()

    count = 0
    right_answer = 0
    for file_name in file_names:
        with open(os.path.join(valid_dir_name, file_name)) as file:
            text = file.read()

        tokens = tokenizer.tokens_count(text)
        probabilities = classificator.classify(tokens.keys())
        print(probabilities)
        probable_class = max_value_key(probabilities)
        if probable_class == class_name:
            right_answer += 1
        count += 1

    print(right_answer)
    print(count - right_answer)
    print(count)
    print(right_answer / float(count) * 100)
