from os import remove, listdir, rename

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
                            new_file.write('cp /home/onedegree/server/ixt_bypass_issue.txt ./ixt_bypass_issue.txt\n')
                            new_file.write('\n')
                        new_file.write(line)
                    else:
                        new_file.write(line)
                    previous_line_2 = previous_line
                    previous_line = line
        remove(input_filename)
        rename("new_" + input_filename, input_filename)



