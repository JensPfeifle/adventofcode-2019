class Instruction:
    pass


class AddInstruction(Instruction):
    len_parameters = 3
    opcode = 1

    def execute(self, intcode):
        pos1 = intcode.memory[intcode.inst_ptr + 1]
        pos2 = intcode.memory[intcode.inst_ptr + 2]
        result_pos = intcode.memory[intcode.inst_ptr + 3]
        intcode.memory[result_pos] = intcode.memory[pos1] + intcode.memory[pos2]
        return intcode.inst_ptr + self.len_parameters + 1


class MultiplyInstruction(Instruction):
    len_parameters = 3
    opcode = 2

    def execute(self, intcode):
        pos1 = intcode.memory[intcode.inst_ptr + 1]
        pos2 = intcode.memory[intcode.inst_ptr + 2]
        result_pos = intcode.memory[intcode.inst_ptr + 3]
        intcode.memory[result_pos] = intcode.memory[pos1] * intcode.memory[pos2]
        return intcode.inst_ptr + self.len_parameters + 1


class HaltInstruction(Instruction):
    len_parameters = 0
    opcode = 99

    def execute(self, intcode):
        intcode.halted = True
        return intcode.inst_ptr + self.len_parameters + 1


class IntCode:
    def __init__(self, program):
        self.program = program
        self.memory = program.copy()
        self.inst_ptr = 0
        self.halted = False

    def __repr__(self):
        return str(self.memory)

    def _get_instruction(self, instruction_code: int):
        try:
            return next(
                cls()
                for cls in Instruction.__subclasses__()
                if cls.opcode == instruction_code
            )
        except StopIteration:
            print("Unkown opcode! Halting.")
            return self._get_instruction(99)

    def step(self):
        opcode = self.memory[self.inst_ptr]
        instruction = self._get_instruction(opcode)
        self.inst_ptr = instruction.execute(intcode=self)

    def run_to_halt(self):
        while True:
            if self.halted:
                break
            self.step()
