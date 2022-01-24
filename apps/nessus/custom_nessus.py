import utils.custom_csv
import utils.custom_json as utils_json
import sqlite3


def write_en_report(input_filename, output_filename):
    temp_list = utils.custom_csv.read_file_to_dict(input_filename)
    result_dict = {}
    final_dict = []
    for temp in temp_list:
        if temp['Name'] not in result_dict:
            result_dict.update({temp['Name']: {
                'Name': temp['Name'],
                'Plugin ID': temp['Plugin ID'],
                'IP': [],
                'Risk': temp['Risk'],
                'CVE': temp['CVE'],
                'Description': temp['Description'],
                'Solution': temp['Solution']
            }})
        result_dict[temp['Name']]['IP'].append(temp['Host'] + ':' + temp['Port'])

    # sort
    temp_c = []
    temp_h = []
    temp_m = []
    temp_l = []
    temp_n = []

    for result in result_dict:
        if result_dict[result]['Risk'] == 'Critical':
            temp_c.append(result_dict[result])
        elif result_dict[result]['Risk'] == 'High':
            temp_h.append(result_dict[result])
        elif result_dict[result]['Risk'] == 'Medium':
            temp_m.append(result_dict[result])
        elif result_dict[result]['Risk'] == 'Low':
            temp_l.append(result_dict[result])
        else:
            temp_n.append(result_dict[result])

    for temp_dict in temp_c:
        final_dict.append(temp_dict)
    for temp_dict in temp_h:
        final_dict.append(temp_dict)
    for temp_dict in temp_m:
        final_dict.append(temp_dict)
    for temp_dict in temp_l:
        final_dict.append(temp_dict)
    for temp_dict in temp_n:
        final_dict.append(temp_dict)

    for temp_result in final_dict:
        print(temp_result)

    utils_json.write_dict_to_file(output_filename, final_dict)


def write_cn_report(input_filename, output_filename):
    temp_list = utils.custom_csv.read_file_to_dict(input_filename)
    result_dict = {}
    final_dict = []
    for temp in temp_list:
        if temp['Name'] not in result_dict:
            temp_search = read_sqlite_select(temp['Plugin ID'])
            if len(temp_search) > 0:
                temp['Name'] = temp_search[1]
                temp['Description'] = temp_search[3]
                temp['Solution'] = temp_search[4]
                pass

            result_dict.update({temp['Name']: {
                'Name': temp['Name'],
                'Plugin ID': temp['Plugin ID'],
                'IP': [],
                'Risk': temp['Risk'],
                'CVE': temp['CVE'],
                'Description': temp['Description'],
                'Solution': temp['Solution']
            }})
        result_dict[temp['Name']]['IP'].append(temp['Host'] + ':' + temp['Port'])

    # sort
    temp_c = []
    temp_h = []
    temp_m = []
    temp_l = []
    temp_n = []
    for result in result_dict:
        if result_dict[result]['Risk'] == 'Critical':
            temp_c.append(result_dict[result])
        elif result_dict[result]['Risk'] == 'High':
            temp_h.append(result_dict[result])
        elif result_dict[result]['Risk'] == 'Medium':
            temp_m.append(result_dict[result])
        elif result_dict[result]['Risk'] == 'Low':
            temp_l.append(result_dict[result])
        else:
            temp_n.append(result_dict[result])
    for temp_dict in temp_c:
        final_dict.append(temp_dict)
    for temp_dict in temp_h:
        final_dict.append(temp_dict)
    for temp_dict in temp_m:
        final_dict.append(temp_dict)
    for temp_dict in temp_l:
        final_dict.append(temp_dict)
    for temp_dict in temp_n:
        final_dict.append(temp_dict)

    for temp_result in final_dict:
        print(temp_result)

    utils_json.write_dict_to_file(output_filename, final_dict)


def read_sqlite_select(input_id):
    conn = sqlite3.connect("vuln.db")
    conn.text_factory = lambda x: str(x, 'gbk', 'ignore')
    # conn.text_factory = str
    result_temp = []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM VULNDB")
        table_list = cursor.fetchall()
        for table in table_list:
            if str(table[0]) == str(input_id):
                result_temp = table
    except Exception as e:
        print(e)
    # conn.text_factory = str
    conn.close()
    return result_temp


if __name__ == '__main__':
    write_en_report("nessus_host_scan_samepl.csv", "sample_en.json")
    # write_cn_report("nessus_host_scan_samepl.csv", "sample_cn.json")
