import chipwhisperer as cw
import argparse

devices = {
    0: '44203120394d36433230312032303032',
    1: '50203120324136503230342037313038'
}

# parse tcas seed file
def parse_file(filename):
    with open(filename, 'r') as f:
        text = f.read()
    text = text.split('\n')

    path_to_tests_dict = {}
    current_tests = []
    current_path = text[0].split('/')[-1].split('.')[0]
    for line in text[1:]:
        if line[:4] == 'File':
            path_to_tests_dict[current_path] = current_tests 
            current_path  =line.split('/')[-1].split('.')[0]
            current_tests = []
        else:
            # current_tests.append(line.split('  ')[-1])
            current_tests.append(' '.join(line.split('\t')[1].split()))
    path_to_tests_dict[current_path] = current_tests
    return path_to_tests_dict

def connect(device_id):
    # init scope and target
    scope = cw.scope(sn=devices[device_id])
    target = cw.target(scope)
    
    # setup scope parameters
    scope.gain.gain = 45
    scope.adc.samples = 2000
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
    return scope, target

def send(text):
    target.simpleserial_write('p', text)
    response = target.simpleserial_read('r', 16)
    return response

def dis():
    scope.dis()
    target.dis()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='power signal acquisition')
    parser.add_argument('-s', default='seed.txt', type=str, help='seed file')
    parser.add_argument('-i', default=0, type=int, help='device id')
    arg = parser.parse_args()

    scope, target = connect(device_id=arg.i)
    seed = parse_file(arg.s)
