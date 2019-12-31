from collections import namedtuple
import logging

#_logger.basicConfig(format='%(levelname)s:%(message)s', level=_logger.DEBUG)


_logger = logging.getLogger("intcode")
_logger.setLevel(logging.DEBUG)

Argument = namedtuple("Argument", "address, value, mode")

class Instruction:
    pass


class AddInstruction(Instruction):
    len_parameters = 3
    opcode = 1

    def execute(self, intcode, args):
        _logger.debug(f"add {args[0].value}, {args[1].value} & store in {args[2].address}")
        result_pos = args[2].address
        intcode.memory[result_pos] = args[0].value + args[1].value
        return intcode.inst_ptr + self.len_parameters + 1


class MultiplyInstruction(Instruction):
    len_parameters = 3
    opcode = 2

    def execute(self, intcode, args):
        _logger.debug(f"multiply {args[0].value}, {args[1].value} & store in {args[2].address}")
        result_pos = args[2].address
        intcode.memory[result_pos] = args[0].value * args[1].value
        return intcode.inst_ptr + self.len_parameters + 1


class SaveInstruction(Instruction):
    len_parameters = 1
    opcode = 3

    def execute(self, intcode, args):
        result_pos = args[0].address
        inpt = int(intcode.stdinput.pop(0))
        _logger.debug(f"store {inpt} from stdin at {result_pos}")
        intcode.memory[result_pos] = inpt
        return intcode.inst_ptr + self.len_parameters + 1

class OutputInstruction(Instruction):
    len_parameters = 1
    opcode = 4

    def execute(self, intcode, args):
        #outpt = intcode.memory[args[0].value]
        outpt = args[0].value
        intcode.stdoutput.append(outpt)
        _logger.debug(f"output {outpt} to std out")
        return intcode.inst_ptr + self.len_parameters + 1

class JumpIfTrueInstruction(Instruction):
    """
    if the first parameter is non-zero, it sets the instruction pointer
    to the value from the second parameter. Otherwise, it does nothing.
    """
    len_parameters = 2
    opcode = 5

    def execute(self, intcode, args):
        check_value = args[0].value
        jump_to_addr = args[1].value
        if not check_value == 0:
            _logger.debug(f"{check_value} is True, jump to {jump_to_addr}")
            return jump_to_addr
        _logger.debug(f"{check_value} is False, no jump")
        return intcode.inst_ptr + self.len_parameters + 1

class JumpIfFalseInstruction(Instruction):
    """
    if the first parameter is zero, it sets the instruction pointer
    to the value from the second parameter. Otherwise, it does nothing.
    """
    len_parameters = 2
    opcode = 6

    def execute(self, intcode, args):
        check_value = args[0].value
        jump_to_addr = args[1].value
        if check_value == 0:
            _logger.debug(f"{check_value} is False, jump to {jump_to_addr}")
            return jump_to_addr
        _logger.debug(f"{check_value} is True, no jump")
        return intcode.inst_ptr + self.len_parameters + 1


class LessThanInstruction(Instruction):
    """
    if the first parameter is less than the second parameter, 
    it stores 1 in the position given by the third parameter. 
    Otherwise, it stores 0.
    """
    len_parameters = 3
    opcode = 7

    def execute(self, intcode, args):
        check_value_1 = args[0].value
        check_value_2 = args[1].value
        result_addr = args[2].address
        if check_value_1 < check_value_2:
            _logger.debug(f"{check_value_1} < {check_value_2}, store 1 in {result_addr}")
            intcode.memory[result_addr] = 1
        else:
            _logger.debug(f"{check_value_1} >= {check_value_2}, store 0 in {result_addr}")
            intcode.memory[result_addr] = 0
        return intcode.inst_ptr + self.len_parameters + 1


class EqualsInstruction(Instruction):
    """
    if the first parameter is equal to the second parameter,
    it stores 1 in the position given by the third parameter. 
    Otherwise, it stores 0.
    """
    len_parameters = 3
    opcode = 8

    def execute(self, intcode, args):
        check_value_1 = args[0].value
        check_value_2 = args[1].value
        result_addr = args[2].address
        if check_value_1 == check_value_2:
            _logger.debug(f"{check_value_1} == {check_value_2}, store 1 in {result_addr}")
            intcode.memory[result_addr] = 1
        else:
            _logger.debug(f"{check_value_1} != {check_value_2}, store 0 in {result_addr}")
            intcode.memory[result_addr] = 0
        return intcode.inst_ptr + self.len_parameters + 1


class HaltInstruction(Instruction):
    len_parameters = 0
    opcode = 99

    def execute(self, intcode, args):
        #assert len(args) == 0
        intcode.halted = True
        _logger.debug(f"halting")
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
        result = []
        while True:
            if self.halted:
                break
            self.step()
            if output_to_console:
                while self.stdoutput:
                    print(self.stdoutput.pop())
            else:
                while self.stdoutput:
                    result.append(self.stdoutput.pop())

        if not output_to_console:
            return result

