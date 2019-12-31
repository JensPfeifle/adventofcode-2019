import logging
from intcode import IntCode
import itertools

logging.basicConfig()
intcodelogger = logging.getLogger("intcode")
intcodelogger.setLevel(logging.INFO)

INPUT_FILE = "day07.inp"

def read(filename, split_on="\n", cast_func = None):
    """ Read and clean up input file """
    with open(filename, "r") as f:
        inpt = f.read().strip().split(split_on)
    if cast_func:
        return list(map(cast_func, inpt))
    return inpt

def settings_for_max_output(amp_software):
    "try phase settings to find highest thruster output"
    largest_signal = 0
    for phase_setting in itertools.permutations([0,1,2,3,4]):
        thr_sig = thruster_signal(phase_setting, amp_software)
        if thr_sig > largest_signal:
            largest_signal = thr_sig
            setting_for_largest = phase_setting
    return setting_for_largest

def amp_stage_signal(phase_setting, input_signal, amp_software):
    computer = IntCode(amp_software)
    computer.stdinput = [phase_setting, input_signal]
    phase_signal = computer.run_to_halt(output_to_console=False)
    return phase_signal.pop()

def thruster_signal(phase_settings, amp_software):
    " calculate thruster output by running settings through the control program"
    ampA_output = amp_stage_signal(phase_settings[0], 0,           amp_software)
    ampB_output = amp_stage_signal(phase_settings[1], ampA_output, amp_software)
    ampC_output = amp_stage_signal(phase_settings[2], ampB_output, amp_software)
    ampD_output = amp_stage_signal(phase_settings[3], ampC_output, amp_software)
    ampE_output = amp_stage_signal(phase_settings[4], ampD_output, amp_software)
    return ampE_output


def tests():
    testprogram = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    phase_settings = settings_for_max_output(testprogram)
    signal = thruster_signal(phase_settings, testprogram)
    assert signal == 43210
    assert phase_settings == (4,3,2,1,0)
    
    testprogram = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
                   101,5,23,23,1,24,23,23,4,23,99,0,0]
    phase_settings = settings_for_max_output(testprogram)
    signal = thruster_signal(phase_settings, testprogram)
    assert signal == 54321
    assert phase_settings == (0,1,2,3,4)

    testprogram = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                   1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    phase_settings = settings_for_max_output(testprogram)
    signal = thruster_signal(phase_settings, testprogram)
    assert signal == 65210
    assert phase_settings == (1,0,4,3,2)

if __name__ == "__main__":
    INPUT = read(INPUT_FILE,split_on=",",cast_func=int)
    tests()
    print("part1")
    phase_settings = settings_for_max_output(INPUT)
    signal = thruster_signal(phase_settings, INPUT)
    print(f"{phase_settings} -> {signal}")
    print("part2")
