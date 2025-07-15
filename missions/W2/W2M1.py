from multiprocessing import Pool
import time

def work_log(args):
    process_name = args[0]
    n = args[1]
    print(f'Process {process_name} waiting {n} seconds')
    time.sleep(n)
    print(f'Process {process_name} Finished.')

def work_log_2(process_name, n):
    print(f'Process {process_name} waiting {n} seconds')
    time.sleep(n)
    print(f'Process {process_name} Finished.')

if __name__ == "__main__":
    with Pool(processes=2) as p:
        p.map(work_log, [('A', 5), ('B', 2), ('C', 1), ('D', 3)])
        #p.starmap(work_log_2, [('A', 5), ('B', 2), ('C', 1), ('D', 3)])