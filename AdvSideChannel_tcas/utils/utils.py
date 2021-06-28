import os
import sys
import ast
import subprocess

import ipdb

PROJECT_DIR = os.getcwd()
SOURCE_DIR = os.path.join(PROJECT_DIR, 'firmware', 'simpleserial-main')

def program_reset():
    current_dir = os.getcwd()
    os.chdir(SOURCE_DIR)
    subprocess.call(['cp', 'simpleserial-main_benign.s', 'simpleserial-main.s'])
    output = subprocess.run(["sh", "windows_make_binary.sh", "main"], capture_output=True)
    if output.stderr != b'':
        print('build failed with {}'.format(output.stderr))
        sys.exit()
    else:
        output = subprocess.run(["st-flash", "--reset", "--format", "ihex", "write", "./simpleserial-main-CW308_STM32F3.hex"], capture_output=True)
        if output.stderr.split()[-1] != b'good!':
            print('flash failed with {}'.format(output.stderr))
            sys.exit()
    
    os.chdir(current_dir)
    print('----------------finished reseting the program!---------------------')

def read_results(result_dir):
    with open(result_dir, 'r') as f:
        res = f.read()
    res = res.strip().split('\n')
    injections = []
    scores_mean = []
    scores_std = []

    for r in res:
        inj, scores = r.split(':')
        injections.append(ast.literal_eval(inj))
        m, s = scores.split(',')
        scores_mean.append(ast.literal_eval(m.strip()))
        scores_std.append(ast.literal_eval(s.strip()))
    
    return injections, scores_mean, scores_std