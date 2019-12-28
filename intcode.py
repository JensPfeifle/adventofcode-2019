from collections import namedtuple
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

Argument = namedtuple("Argument", "address, value, mode")

class Instruction:
    pass


class AddInstruction(Instruction):
    len_parameters = 3
    opcode = 1

    def execute(self, intcode, args):
        logging.debug(f"Add {args[0].value}, {args[1].value} & store in {args[2].address}")
        result_pos = args[2].address
        intcode.memory[result_pos] = args[0].value + args[1].value
        return intcode.inst_ptr + self.len_parameters + 1


class MultiplyInstruction(Instruction):
    len_parameters = 3
    opcode = 2

    def execute(self, intcode, args):
        logging.debug(f"Multiply {args[0].value}, {args[1].value} & store in {args[2].address}")
        result_pos = args[2].address
        intcode.memory[result_pos] = args[0].value * args[1].value
        return intcode.inst_ptr + self.len_parameters + 1


class SaveInstruction(Instruction):
    len_parameters = 1
    opcode = 3

    def execute(self, intcode, args):
        result_pos = args[0].address
        inpt = int(intcode.stdinput.pop())
        logging.debug(f"Store {inpt} from stdin at {result_pos}")
        intcode.memory[result_pos] = inpt
        return intcode.inst_ptr + self.len_parameters + 1

class OutputInstruction(Instruction):
    len_parameters = 1
    opcode = 4

    def execute(self, intcode, args):
        outpt = intcode.memory[args[0].address]
        logging.debug(f"generated standard output {outpt}")
        intcode.stdoutput.append(outpt)
        logging.debug(f"Output {outpt} to std out")
        return intcode.inst_ptr + self.len_parameters + 1


class HaltInstruction(Instruction):
    len_parameters = 0
    opcode = 99

    def execute(self, intcode, args):
        #assert len(args) == 0
        intcode.halted = True
        logging.debug(f"halting")
        return None


class IntCode:
    def __init__(self, program):
        self.program = program
        self.memory = program.copy()
        self.inst_ptr = 0
        self.halted = False
        self.stdinput = []
        self.stdoutput = []

    def __repr__(self):
        return str(self.memory)

    def _get_instruction(self, instruction_code: int):
        try:
            return next(
                cls()
                for cls in Instruction.__subclasses__()
                if cls.opcode == int(instruction_code)
            )
        except StopIteration:
            print(f"Unkown opcode {instruction_code}! Halting.")
            return self._get_instruction(99)

    def _parse_arguemnts(self, argument_num):
        modes = list(reversed(str(self.memory[self.inst_ptr])[:-2].zfill(argument_num)))
        arguments = []
        for i, mode in enumerate(modes):
            if mode == '0':
                # position mode
                addr = self.memory[self.inst_ptr + 1 + i]
                val = self.memory[addr]
                arg = Argument(address = int(addr), value = int(val), mode=mode)
                arguments.append(arg)
            elif mode == '1':
                # immediate mode
                val = self.memory[self.inst_ptr  + 1 + i]
                # address = val the right choice here? better None?
                arg = Argument(address = int(val), value = int(val), mode=mode)
                arguments.append(arg)
            else:
                print(f"unkown argument mode {mode}!")
        return arguments

    def step(self):
        opcode = str(self.memory[self.inst_ptr])[-2:]
        instruction = self._get_instruction(opcode)
        arguments = self._parse_arguemnts(instruction.len_parameters)
        self.inst_ptr = instruction.execute(intcode=self, args=arguments)

    def run_to_halt(self, output_to_console = True):
        while True:
            if self.halted:
                break
            self.step()
            if output_to_console:
                while self.stdoutput:
                    print(self.stdoutput.pop())
