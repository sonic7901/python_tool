import csv


def read_file_to_dict(input_filename):
    list_dict = []
    with open(input_filename, mode='r', encoding="utf-8") as csv_file:
        rows = csv.reader(csv_file)
        count = 0
        name_list = []
        for row in rows:
            temp_dict = {}
            if count == 0:
                name_list = row
            else:
                for i in range(0, len(name_list)):
                    temp_dict[name_list[i]] = row[i]
                list_dict.append(temp_dict)
            count += 1
    return list_dict


if __name__ == '__main__':
    pass
