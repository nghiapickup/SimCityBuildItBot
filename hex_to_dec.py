with open('get_event.input', 'r') as f:
    lines = f.readlines()
    lines = [line.strip().split(' ') for line in lines]
    for line in lines:
        if len(line) != 4: print(f'error line! {line}')
        print(line[0].strip(':'), *map(lambda x: int(x, 16), line[1:]))