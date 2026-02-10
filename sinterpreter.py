import sys


class SInterpreter:
    def __init__(self) -> None:
        self._stack: list[str] = []  # Stack to hold intermediate values
        self.variable_storage: dict[str, int] = {}  # Holds values of variables
        self.COMMANDS = {
            "ADD": self._add,
            "SUB": self._sub,
            "MULT": self._mult,
            "ASSIGN": self._assign,
            "PRINT": self._print,
        }

    # The fetch-decode-execute cycle
    def cycle(self) -> None:
        # Fetch
        for line in sys.stdin:
            line: str = line.rstrip("\n")
            operations: list[str] = line.split()
            if not line:
                continue

            if operations[0] == "PUSH":
                self._push(operations[1])
            elif operations[0] in self.COMMANDS:
                self.COMMANDS[operations[0]]()

    # The intermediate language consists of the following commands:

    # PUSH op : pushes the operand op onto the stack.
    # ADD : pops the two top elements from the stack, adds their values
    #       and pushes the result back onto the stack.
    # SUB : pops the two top elements from the stack, subtracts the first
    #       value retrieved from the second value,
    #       and pushes the result back onto the stack.
    # MULT : pops the two top elements from the stack, multiplies their
    #        values and pushes the result back onto the stack.
    # ASSIGN : pops the two top elements from the stack, assigns the first
    #          element (a value) to the second element (a variable).
    # PRINT : prints the value currently on top of the stack.

    def _pop_var_from_stack(self) -> int:
        var: str | int = self._stack.pop()
        if var in self.variable_storage:
            return self.variable_storage[var]
        else:
            try:
                return int(var)
            except ValueError:
                raise ValueError(
                    f"Variable {var} not found in storage and cannot be converted to int."
                )

    def _push(self, op: str) -> None:
        # Pushes the operand op onto the stack.
        self._stack.append(op)

    def _add(self) -> None:
        # Pops the two top elements from the stack, adds their values and
        # pushes the result back onto the stack.
        var1: int = self._pop_var_from_stack()
        var2: int = self._pop_var_from_stack()
        self._push(str(var1 + var2))

    def _sub(self) -> None:
        # Pops the two top elements from the stack, subtracts the first value
        # retrieved from the second value, and pushes the result back onto the
        # stack.
        var1: int = self._pop_var_from_stack()
        var2: int = self._pop_var_from_stack()
        self._push(str(var1 - var2))

    def _mult(self) -> None:
        # Pops the two top elements from the stack, multiplies their values and
        # pushes the result back onto the stack.
        var1: int = self._pop_var_from_stack()
        var2: int = self._pop_var_from_stack()
        self._push(str(var1 * var2))

    def _assign(self) -> None:
        # Pops the two top elements from the stack, assigns the first element
        # (a value) to the second element (a variable).
        var1: int = self._pop_var_from_stack()
        var2: str = self._stack.pop()
        self.variable_storage[var2] = var1

    def _print(self) -> None:
        # Prints the value currently on top of the stack.
        print(self._stack.pop())


# I have to use a stack(can use a list) here to process the intermediate code.

# What the interpreter does in programming languages here is to *execute* the
# intermediate code.
# It will fetch the next instruction, decode it, and then execute it.
# The stack is used to keep track of intermediate values during execution.


def main() -> None:
    interpreter = SInterpreter()
    interpreter.cycle()


if __name__ == "__main__":
    main()
