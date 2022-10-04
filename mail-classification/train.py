import json
import os
from typing import Dict

import dotenv

from default_const import default_train_data_list_file_name
from tokenizer import Tokenizer
from collections import Counter

default_freq_dict_save_file_name = "freq_dict.json"

train_data_list_file_name = None
class FreqData:
    def __init__(self, class_name: str, text: str):
        self.class_name = class_name
        self.text = text

class FreqDict:
    def __init__(self):
        self._tokenizer = Tokenizer.default_tokenizer()
        self._bag_of_words = {}
        self._classes = {}
    def accumulate(self, data: FreqData):
        tokens_count = self._tokenizer.tokens_count(data.text)
        class_name = data.class_name

        for token, count in tokens_count.items():
            if token in self._bag_of_words:
                token_dict = self._bag_of_words[token]

                if class_name in token_dict:
                    token_dict[class_name].update(self._counter_dict(count))
                else:
                    token_dict[class_name] = self._counter(count)
            else:
                self._bag_of_words[token] = {
                    class_name: self._counter(count)
                }

        if class_name in self._classes:
            self._classes[class_name] = self._classes[class_name] + 1
        else:
            self._classes[class_name] = 1

    @staticmethod
    def _counter_dict(count):
        return {
            "dc": 1,
            "wc": count
        }

    def _counter(self, count):
        return Counter(self._counter_dict(count))

    def json_dict(self) -> Dict:
        json_dict = {"data": self._bag_of_words, "classes": self._classes}
        return json_dict

def fill_freq_dict(freq_dict: FreqDict, dir: str, class_name: str):
    with open (os.path.join(dir, train_data_list_file_name), 'r') as list_file:
        files = list_file.read().split()

    for file_name in files:
        with open(os.path.join(dir, file_name), 'r') as file:
            text = file.read()
        freq_data = FreqData(class_name, text)

        freq_dict.accumulate(freq_data)

def append_data(dict, words_freq, class_name):
    for word, count in words_freq.items():
        if word in dict:
            dict[word].update({class_name: count})
        else:
            dict[word] = {class_name: count}

def words_freq(dir: str) -> FreqDict:
    freq_dict = FreqDict()

    for path in os.scandir(dir):
        if (os.path.isdir(path)):
            class_dir = path
            class_name = path.name
            fill_freq_dict(freq_dict, class_dir, class_name)

    return freq_dict

def save_to_json(freq_dict: Dict, file: str):
    with open(file, 'w') as json_file:
        json.dump(freq_dict, json_file)

if __name__ == '__main__':
    dotenv.load_dotenv()

    data_root_dir = os.environ["data_root_dir"]
    train_data_list_file_name = os.environ.get("train_data_list_file_name", default_train_data_list_file_name)
    freq_dict_path = os.environ.get("freq_dict_file_name")
    if freq_dict_path is None:
        freq_dict_path = os.path.join(data_root_dir, default_freq_dict_save_file_name)
    else:
        freq_dict_path = os.path.join(freq_dict_path)

    words_freq = words_freq(data_root_dir)
    save_to_json(words_freq.json_dict(), freq_dict_path)