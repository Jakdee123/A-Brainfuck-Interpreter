class backend:
    ascii_table = [chr(i) for i in range(256)]  # Including character for index 255
    mem_array = [0] * 33000
    mem_index = 0  # Starting at 0 for Python's zero-based indexing
    arg = ""
    arg_index = 0
    arg_curr = arg[arg_index] if arg else None  # Check if arg is not empty
    first_arg_read = True
    code = ""  # Brainfuck code should be placed here
    code_index = 0
    output_result = ""  # Renamed to avoid conflict with the output function
    arg_err = False
    need_arg = False
    invalid_char_found = False
    command = 0

    @staticmethod
    def add():
        if backend.mem_array[backend.mem_index] == 255:
            backend.mem_array[backend.mem_index] = 0
        else:
            backend.mem_array[backend.mem_index] += 1

    @staticmethod
    def sub():
        if backend.mem_array[backend.mem_index] == 0:
            backend.mem_array[backend.mem_index] = 255
        else:
            backend.mem_array[backend.mem_index] -= 1

    @staticmethod
    def right():
        backend.mem_index += 1
        if backend.mem_index >= 33000:
            backend.mem_index = 0

    @staticmethod
    def left():
        backend.mem_index -= 1
        if backend.mem_index <= 0:
            backend.mem_index = 33000

    @staticmethod
    def output_char():
        backend.output_result += backend.ascii_table[backend.mem_array[backend.mem_index]]


    @staticmethod
    def read_arg():
        if backend.first_arg_read:
            backend.first_arg_read = False
        else:
            backend.arg_index += 1
        if backend.arg_index < len(backend.arg):
            backend.arg_curr = backend.arg[backend.arg_index]
        else:
            backend.arg_index = 1
        backend.mem_array[backend.mem_index] = backend.ascii_table.find(backend.arg_curr)

    func_map = {
        '>': right,
        '<': left,
        '+': add,
        '-': sub,
        '.': output_char,
        ',': read_arg,
    }

    loop_stack = []

    @staticmethod
    def run():
        backend.arg_curr = backend.arg[0] if backend.arg else None

        while backend.code_index < len(backend.code):
            command = backend.code[backend.code_index]

            if command in backend.func_map:
                backend.func_map[command]()
            elif command == "[":
                if backend.mem_array[backend.mem_index] == 0:
                    loop_start = backend.code_index
                    depth = 1
                    while depth > 0:
                        backend.code_index += 1
                        if backend.code[backend.code_index] == "[":
                            depth += 1
                        elif backend.code[backend.code_index] == "]":
                            depth -= 1
                else:
                    backend.loop_stack.append(backend.code_index)
            elif command == "]":
                if backend.mem_array[backend.mem_index] != 0:
                    backend.code_index = backend.loop_stack[-1]
                else:
                    backend.loop_stack.pop()
            else:
                pass
            backend.code_index += 1

def run_code():
    code_text = "++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++.>+.+++++++..+++.<<++++++++++++++.------------.>+++++++++++++++.>.+++.------.--------.<<+."
    arg_text = ""
    need_arg = False
    invalid_arg_char = False
    err_code = None
    finde = 0

    backend.code = code_text
    backend.arg = arg_text


    finde = backend.code.find(",")
    if finde != -1:
        need_arg = True
    else:
        need_arg = False


    if need_arg and not arg_text:
        print("Argument Error 1: The program requires an argument but has not been given one")
        err_code = 1

    # Check if the argument contains invalid characters
    if need_arg:
        for char in backend.arg:
            if char not in backend.ascii_table:
                print("Argument Error 2: A character in the argument is not a valid character in Brainfuck")
                err_code = 2
    else:
        pass



    if err_code == 1:
        print("ERR 1")
    elif err_code == 2:
        print("ERR 2")
    else:
        backend.run()
        print(f"Output: {backend.output_result}")




run_code()
