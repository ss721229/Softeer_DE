from multiprocessing import Process

def work_log(continent='Asia'):
    print(f'The name of continent is : {continent}')

if __name__ == "__main__":
    process_1 = Process(target=work_log, args=('America',))
    process_2 = Process(target=work_log)
    process_3 = Process(target=work_log, args=('Europe',))
    process_4 = Process(target=work_log, args=('Africa',))

    process_1.start()
    process_2.start()
    process_3.start()
    process_4.start()

    process_1.join()
    process_2.join()
    process_3.join()
    process_4.join()