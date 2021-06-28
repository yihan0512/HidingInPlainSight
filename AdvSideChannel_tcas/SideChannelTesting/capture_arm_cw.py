# To be used with seed files generated from KLEE CLI output
from __future__ import division, print_function

import time
from datetime import date
import os
import argparse
import sys

import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
from tqdm import tqdm, trange 

import chipwhisperer as cw

import ipdb

devices = {
    0: '44203120394d36433230312032303032',
    1: '50203120324136503230342037313038'
}

# parse dijkstra seed file
# def parse_file(filename):
#     with open(filename, 'r') as f:
#         text = f.read()
#     testcases = text.split('File')[1:]
#     testcases_new = dict()
#     for testcase in testcases:
#         key = testcase.split('smt2\n')[0][2:-1]
#         value = testcase.split('smt2\n')[1].split('\n')[:-1]
#         value_new = []
#         for tc in value:
#             try:
#                 text = tc.split('\t')[1].strip()
#             except:
#                 print(testcase.split('smt2\n'))
#             value_new.append(text)
#         testcases_new[key] = value_new
#     return testcases_new

# parse tcas seed file
def parse_file(filename):
    with open(filename, 'r') as f:
        text = f.read()
    text = text.split('\n')

    path_to_tests_dict = {}
    current_tests = []
    current_path = text[0].split('/')[-1]
    for line in text[1:]:
        if line[:4] == 'File':
            path_to_tests_dict[current_path] = current_tests 
            current_path  =line.split('/')[-1]
            current_tests = []
        else:
            # current_tests.append(line.split('  ')[-1])
            current_tests.append(' '.join(line.split('\t')[1].split()))
    path_to_tests_dict[current_path] = current_tests
    return path_to_tests_dict

def capture_all(N, Nt, seed, root, device_id=0):
    # init scope and target
    scope = cw.scope(sn=devices[device_id])
    target = cw.target(scope)
    
    # setup scope parameters
    scope.gain.gain = 45
    scope.adc.samples = 20000
    scope.adc.offset = 0
    scope.adc.basic_mode = "rising_edge"
    scope.clock.clkgen_freq = 10000000
    scope.clock.adc_src = "clkgen_x4"
    scope.trigger.triggers = "tio4"
    scope.io.tio1 = "serial_rx"
    scope.io.tio2 = "serial_tx"
    scope.io.hs2 = "clkgen"

    # setup target parameters
    target.baud = 115200


    # manual target reset
    # input('Please reset the target...')
    
    # generate testcases
    try:
        testcase = parse_file(seed)
    except:
        print(os.getcwd())
        ipdb.set_trace()
    testcase_list = list(testcase.items())
    testcase_list.sort()

    # create root dir for saving data
    if not os.path.exists(root):
        os.mkdir(root)

    # for each path
    for path in trange(N):
        seed = testcase_list[path]

        if not os.path.exists(os.path.join(root, seed[0])):
            os.mkdir(os.path.join(root, seed[0]))

        # for each test case 
        count = 0
        # for i in trange(len(seed[1]), desc='Capturing testcases'):
        for i in range(len(seed[1])):
            text = seed[1][i]
            # tqdm.write("# %d testcase: %s" % (i, text))

            trace_testcase = []
            trigger_testcase = []

            # for j in trange(arg.Nt, desc='Capturing traces'):
            for j in range(Nt):
                captured = cw.capture_trace(scope, target, text)
                if not captured:
                    print('Target stopped working! Current input: {}'.format(text))
                    return True
                trace, trig = captured.wave, captured.trig_count
                trace_testcase.append(trace)
                trigger_testcase.append(trig)

            # get rid of outliers 
            trigger = Counter(trigger_testcase).most_common(1)[0][0]

            # for key in Counter(trigger_testcase).items():
            #     tqdm.write("%i: %i" % (key[0], key[1]))

            trace_testcase_new = []
            for trace, trigger_value in zip(trace_testcase, trigger_testcase):
                if trigger_value == trigger:
                    trace_testcase_new.append(trace)
            while len(trace_testcase_new) != Nt:
                # tqdm.write('making another capture...')
                captured = cw.capture_trace(scope, target, text)
                trace, trig = captured.wave, captured.trig_count
                if trig == trigger:
                    trace_testcase_new.append(trace)
            traces = np.array(trace_testcase_new)[:, :trigger]

            # save to file
            date_string = date.today().strftime('%m%d%Y')
            for i in range(Nt):
                # np.save(os.path.join(root, seed[0], '{0}_{1:0=3d}'.format(date_string, count)+'.npy'), {'trace': traces[i], 'text': text})
                np.save(os.path.join(root, seed[0], '{:0=3d}'.format(count)+'.npy'), {'trace': traces[i], 'text': text})
                count += 1

            # tqdm.write('Data saved to {}'.format(os.path.join(root, seed[0])))
        

    # cleanup the connection to the target and scope
    scope.dis()
    target.dis()
    
    return False
    
def capture_single(Nt, seed, index, root, device_id=0):
    # init scope and target
    scope = cw.scope(sn=devices[device_id])
    target = cw.target(scope)
    
    # setup scope parameters
    scope.gain.gain = 45
    scope.adc.samples = 20000
    scope.adc.offset = 0
    scope.adc.basic_mode = "rising_edge"
    scope.clock.clkgen_freq = 10000000
    scope.clock.adc_src = "clkgen_x4"
    scope.trigger.triggers = "tio4"
    scope.io.tio1 = "serial_rx"
    scope.io.tio2 = "serial_tx"
    scope.io.hs2 = "clkgen"

    # setup target parameters
    target.baud = 115200


    # manual target reset
    # raw_input('Please reset the target...')
    
    # generate testcases
    testcase = parse_file(seed)
    testcase_list = list(testcase.items())
    testcase_list.sort()

    # create root dir for saving data
    if not os.path.exists(root):
        os.mkdir(root)

    seed = testcase_list[index]

    if not os.path.exists(os.path.join(root, seed[0])):
        os.mkdir(os.path.join(root, seed[0]))

    # for each test case 
    count = 0
    # for i in trange(len(seed[1]), desc='Capturing testcases'):
    for i in range(len(seed[1])):
        text = seed[1][i]
        # tqdm.write("# %d testcase: %s" % (i, text))

        trace_testcase = []
        trigger_testcase = []

        # for j in trange(arg.Nt, desc='Capturing traces'):
        for j in range(Nt):
            captured = cw.capture_trace(scope, target, text)
            if not captured:
                print('Target stopped working!')
                return True
            trace, trig = captured.wave, captured.trig_count
            trace_testcase.append(trace)
            trigger_testcase.append(trig)

        # get rid of outliers 
        trigger = Counter(trigger_testcase).most_common(1)[0][0]
        # for key in Counter(trigger_testcase).items():
        #     tqdm.write("%i: %i" % (key[0], key[1]))

        trace_testcase_new = []
        for trace, trigger_value in zip(trace_testcase, trigger_testcase):
            if trigger_value == trigger:
                trace_testcase_new.append(trace)
        while len(trace_testcase_new) != Nt:
            # tqdm.write('making another capture...')
            captured = cw.capture_trace(scope, target, text)
            trace, trig = captured.wave, captured.trig_count
            if trig == trigger:
                trace_testcase_new.append(trace)
        traces = np.array(trace_testcase_new)[:, :trigger]

        # save to file
        for i in range(Nt):
            np.save(os.path.join(root, seed[0], '{0:0=3d}'.format(count)+'.npy'), {'trace': traces[i], 'text': text})
            count += 1

        # tqdm.write('Data saved to {}'.format(os.path.join(arg.root, seed[0])))
        

    # cleanup the connection to the target and scope
    scope.dis()
    target.dis()
    
    return False

def capture_testcase(Nt, seed, path, index, root, device_id=0):
    # init scope and target
    scope = cw.scope(sn=devices[device_id])
    target = cw.target(scope)
    
    # setup scope parameters
    scope.gain.gain = 45
    scope.adc.samples = 20000 
    scope.adc.offset = 0
    scope.adc.basic_mode = "rising_edge"
    scope.clock.clkgen_freq = 10000000
    scope.clock.adc_src = "clkgen_x4"
    scope.trigger.triggers = "tio4"
    scope.io.tio1 = "serial_rx"
    scope.io.tio2 = "serial_tx"
    scope.io.hs2 = "clkgen"

    # setup target parameters
    target.baud = 115200


    # manual target reset
    # raw_input('Please reset the target...')
    
    # generate testcases
    testcase = parse_file(seed)
    testcase_list = list(testcase.items())
    testcase_list.sort()

    # create root dir for saving data
    if not os.path.exists(root):
        os.mkdir(root)

    seed = testcase_list[path]

    if not os.path.exists(os.path.join(root, seed[0])):
        os.mkdir(os.path.join(root, seed[0]))

    # for each test case 
    count = 0
    # tqdm.write("# %d testcase: %s" % (i, text))

    text = seed[1][index]

    trace_testcase = []
    trigger_testcase = []

    # for j in trange(arg.Nt, desc='Capturing traces'):
    for j in range(Nt):
        captured = cw.capture_trace(scope, target, text)
        if not captured:
            print('Target stopped working!')
            return True
        trace, trig = captured.wave, captured.trig_count
        trace_testcase.append(trace)
        trigger_testcase.append(trig)

    # get rid of outliers 
    trigger = Counter(trigger_testcase).most_common(1)[0][0]
    # for key in Counter(trigger_testcase).items():
    #     tqdm.write("%i: %i" % (key[0], key[1]))

    trace_testcase_new = []
    for trace, trigger_value in zip(trace_testcase, trigger_testcase):
        if trigger_value == trigger:
            trace_testcase_new.append(trace)
    while len(trace_testcase_new) != Nt:
        # tqdm.write('making another capture...')
        captured = cw.capture_trace(scope, target, text)
        trace, trig = captured.wave, captured.trig_count
        if trig == trigger:
            trace_testcase_new.append(trace)
    traces = np.array(trace_testcase_new)[:, :trigger]

    # save to file
    for i in range(Nt):
        np.save(os.path.join(root, seed[0], str(count)+'.npy'), {'trace': traces[i], 'text': text})
        count += 1

        # tqdm.write('Data saved to {}'.format(os.path.join(arg.root, seed[0])))
        

    # cleanup the connection to the target and scope
    scope.dis()
    target.dis()
    
    return False

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='power signal acquisition')
    parser.add_argument('-N', default=24, type=int, help='Number of paths')
    parser.add_argument('-Nt', default=20, type=int, help='Number of traces per test input')
    parser.add_argument('-s', '--seed', default='../firmware/simpleserial-main/klee_ifelse.txt', type=str, help='Specify seed file')
    parser.add_argument('-i', '--index', default=0, type=int, help='specify which testcase to collect')
    parser.add_argument('-r', '--root', default='data', type=str, help='specify root dir for save')
    args = parser.parse_args()

    # collect training data 
    ret = capture_all(N=args.N, Nt=args.Nt, seed=args.seed, root=args.root, device_id=0)
    if ret:
        print('trigger missed!')
        sys.exit()