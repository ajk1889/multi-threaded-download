def format_path(path):
    path = path.strip()
    if path[0] in '\'"': path = path[1:]
    if path[-1] in '\'"': path = path[:-1]
    return path

source = format_path(input("First file: "))
source = source[:-1] # to remove trailing 0 (for first file)
destination = format_path(input("Destination: "))
n = int(input("Files count: "))

op = open(destination, 'wb')
total = 0
last_printed_total = 0
for i in range(n):
    ip = open(f'{source}{i}', 'rb')
    read = ip.read(1024*1024)
    while read:
        op.write(read)
        total += len(read)
        if last_printed_total != int(total/1024**2) and int(total/1024**2) % 100 == 0:
            print(int(total/1024**2))
            last_printed_total = int(total/1024**2)
        read = ip.read(1024*1024)
    ip.close()
op.close()