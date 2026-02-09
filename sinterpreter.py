class SInterpreter:
    def __init__(self) -> None:
        pass

    # The fetch-decode-execute cycle
    def cycle(self):
        pass
# I have to use a stack(can use a list) here to process the intermediate code.

# What the interpreter does in programming languages here is to *execute* the
# intermediate code. 
# It will fetch the next instruction, decode it, and then execute it. 
# The stack is used to keep track of intermediate values during execution.