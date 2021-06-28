# regex library
import re
import os
import subprocess
import ipdb

def parse_asm_file(fname):
    label_start_parsing = re.compile("	bl	trigger_high")
    label_stop_parsing = re.compile("	bl	trigger_low")

    # label = re.compile("^[.][a-zA-Z0-9]+:")
    # label = re.compile("^[.]L[0-9]+:")
    label = re.compile("^([.]L.*?|\t[.]loc.*?)")

    with open(fname, "r") as f:
        full_assembly = f.readlines()

    can_loc = []
    for j in range(len(full_assembly)):
        # looking for labels
        if label_start_parsing.match(full_assembly[j]):
            start_line = j
            for i in range(start_line, len(full_assembly)):
                if label_stop_parsing.match(full_assembly[i]):
                    break

                if label.match(full_assembly[i]):
                    continue
                else:
                    can_loc.append(i+1)
    return can_loc

def insert_malware_chunks(my_combs_1, fname, mal_list):
    if len(my_combs_1) != len(mal_list):
        print("number of injection locations and length of malware list mismatch!")
        return True

    # get a clean version of the assembly
    current_dir = os.getcwd()
    home_dir = os.getenv("HOME") 
    os.chdir(os.path.join('firmware', 'simpleserial-main'))
    subprocess.call(['cp', 'simpleserial-main_benign.s', 'simpleserial-main.s'])

    # read assembly code
    with open(fname, 'r') as f:
        full_assembly = f.readlines()

    full_assembly = dict(enumerate(full_assembly, 1))

    for i, line_number in enumerate(my_combs_1):
        full_assembly[line_number] = full_assembly[line_number]+mal_list[i]

    #write out
    modified_asm = "".join(list(zip(*full_assembly.items()))[1])
    with open(fname, 'w') as f:
        f.write(modified_asm)

    # assemble to binary and upload
    output = subprocess.run(['sh', 'windows_make_binary.sh', 'main'], capture_output=True)
    if output.stderr != b'':
        print('build failed with {}'.format(output.stderr))
        os.chdir(current_dir)
        return True 
    # output = subprocess.run(["st-flash", "--reset", "--format", "ihex", "write", "./simpleserial-main-CW308_STM32F3.hex"], capture_output=True)
    output = subprocess.run(['sh', 'windows_make_upload.sh', 'main'], capture_output=True)
    if output.stderr.split()[-1] != b'good!':
        print('flash failed with {}'.format(output.stderr))
        os.chdir(current_dir)
        return True

    os.chdir(current_dir)
    
    return False
    