import requests as req
from multiprocessing import Process, Array
def format_path(path):
    path = path.strip()
    if path[0] in '\'"': path = path[1:]
    if path[-1] in '\'"': path = path[:-1]
    return path

def format(num):
	return "%.2f"%(num/1024**2)
def download(url, offset, limit, file, index, progress):
	header = {"Range": f"bytes={offset}-{limit}"}
	ip = req.get(url, stream=True, headers=header).raw
	op = open(file+str(index), 'wb')
	n = ip.read(8000)
	prev = progress[index]
	while n:
		op.write(n)
		progress[index]+=len(n)
		if(progress[index] - prev > 1024**2):
			prev = progress[index]
			print("\r",' '.join([format(i) for i in progress]), end='')
		n = ip.read(8000)
	ip.close()
	op.close()


url = input("URL: ")
fileName = format_path(input("output file: "))
offset = int(input("offset: "))
numThreads = int(input("Threads: "))
progress = Array('i', range(numThreads))
gbpt = int(float(input("expected GB: "))*1024**3/numThreads)
print("data:", offset, numThreads, gbpt)
processes = []
for i in range(numThreads):
	local_offset = str(offset+gbpt*i)
	local_limit = str(offset+gbpt*(i+1)-1) if i < numThreads-1 else ''
	print("thread:", i, f'|{local_offset}|', f'|{local_limit}|')
	p = Process(target=download, args=(url, local_offset, local_limit, fileName, i, progress))
	p.start()
	processes.append(p)
for p in processes:
	p.join()