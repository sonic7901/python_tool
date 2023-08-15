from os import remove, listdir, rename
import os
from PIL import Image


def static_scan():
    files = listdir(".")
    for file in files:
        input_filename = file
        if '.sh' in input_filename:
            with open(input_filename) as old_file:
                with open("new_" + input_filename, 'w') as new_file:
                    lines = old_file.readlines()
                    previous_line = ''
                    for line in lines:
                        if line == 'docker exec --user root $container_name sourceanalyzer -b Fortify -scan ' \
                                   '-f /scan/$hash.fpr\n':
                            new_file.write('docker exec --user root $container_name sourceanalyzer -b Fortify -scan '
                                           '-filter /scan/$project_name/ixt_bypass_issue.txt -f /scan/$hash.fpr\n')
                        elif line == 'git rev-parse HEAD >> ../../server/$p_name.hash\n':
                            if previous_line_2 == 'rm ../../server/$p_name.hash\n':
                                new_file.write(
                                    'cp /home/onedegree/server/ixt_bypass_issue.txt ./ixt_bypass_issue.txt\n')
                                new_file.write('\n')
                            new_file.write(line)
                        else:
                            new_file.write(line)
                        previous_line_2 = previous_line
                        previous_line = line
            remove(input_filename)
            rename("new_" + input_filename, input_filename)


def check_image_dimensions(input_directory):
    temp_list = []
    for root, _, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                image_path = os.path.join(root, file)
                with Image.open(image_path) as img:
                    width, height = img.size
                    if width != 1080 or height != 1920:
                        print(f"{image_path}: Width = {width}px, Height = {height}px")
                        temp_list.append(image_path)
    for temp_path in temp_list:
        os.remove(temp_path)


if __name__ == "__main__":
    directory = input("請輸入要檢查的資料夾路徑: ")
    check_image_dimensions(directory)
