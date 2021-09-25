# convert getevent from get_event.input to hex code to decimal code

with open('./utils/get_event.input', 'r') as f:
    lines = f.readlines()
    lines = [line.strip().split(' ') for line in lines]
    fun_input = []
    for line in lines:
        if len(line) != 4: print(f'error line! {line}')
        print(line[0].strip(':'), *map(lambda x: int(x, 16), line[1:]))
        fun_input.append(tuple(map(lambda x: int(x, 16), line[1:])))

    print(fun_input)