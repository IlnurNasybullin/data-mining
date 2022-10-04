import os
import random
from typing import Tuple, List

from dotenv import load_dotenv
from default_const import default_train_data_list_file_name
from default_const import default_test_data_list_file_name
from default_const import default_valid_data_list_file_name

default_training_partition = 0.6
default_testing_partition = 0.2

train_data_list_file_name = None
valid_data_list_file_name = None
test_data_list_file_name = None

def write_data_list(dir: str, filename: str, data_list: List[str]):
    with open(os.path.join(dir, filename), 'w') as write_file:
        for data in data_list:
            write_file.write(data + '\n')

def create_data_list(class_dir: str, training_partition: float, testing_partition: float):
    data_files = []
    for path in os.listdir(class_dir):
        if os.path.isfile(os.path.join(class_dir, path)):
            data_files.append(path)

    random.shuffle(data_files)

    files_count = len(data_files)
    training_data_count = int(files_count * training_partition)
    testing_data_count = int(files_count * testing_partition)

    write_data_list(class_dir, train_data_list_file_name, data_files[0:training_data_count + 1])
    write_data_list(class_dir, test_data_list_file_name, data_files[training_data_count + 1:training_data_count + testing_data_count + 1])

    if training_partition + testing_partition < 0.9:
        write_data_list(class_dir, valid_data_list_file_name, data_files[training_data_count + testing_data_count + 1:])

def raise_error_for_open_range(key_name: str, value: float, lower: float, upper: float):
    if value <= lower or value >= upper:
        raise ValueError(f"Illegal value of {key_name} = {value}. It should be more than {lower} and"
                         f"less than {upper}")

def read_partitions() -> Tuple[float, float]:
    training_partition = float(os.environ.get("training_partition", default_training_partition))
    testing_partition = float(os.environ.get("testing_partition", default_testing_partition))

    raise_error_for_open_range("training_partition", training_partition, 0.0, 1.0)
    raise_error_for_open_range("testing_partition", testing_partition, 0.0, 1.0)

    partitions = training_partition + testing_partition
    if partitions > 1.0:
        raise ValueError(f"Sum of partitions can not be more than 1.0")

    return training_partition, testing_partition

if __name__ == '__main__':
    load_dotenv()
    data_root_dir = os.environ["data_root_dir"]

    train_data_list_file_name = os.environ.get("train_data_list_file_name", default_train_data_list_file_name)
    valid_data_list_file_name = os.environ.get("valid_data_list_file_name", default_valid_data_list_file_name)
    test_data_list_file_name = os.environ.get("test_data_list_file_name", default_test_data_list_file_name)

    training_partition, testing_partition = read_partitions()

    files = os.scandir(data_root_dir)
    for inner_path in files:
        if os.path.isdir(inner_path):
            class_dir = inner_path
            create_data_list(class_dir, training_partition, testing_partition)
