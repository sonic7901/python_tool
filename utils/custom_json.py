import json


def read_file_to_dict(input_filename):
    with open(input_filename) as json_file:
        data = json.load(json_file)
        return data


def write_dict_to_file(input_filename, input_dict):
    with open(input_filename, 'w') as fp:
        json.dump(input_dict, fp)


if __name__ == '__main__':
    pass
