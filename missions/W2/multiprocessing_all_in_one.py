"""
- Queue(tasks_to_accomplish)를 사용해 여러 프로세스에서 실행되는 10개의 작업 분배
- tasks_to_accomplish에서 작업 검색, 실행
- 결과를 Queue(tasks_that_are_done)에 저장하는 4개의 프로세스 생성
"""

from multiprocessing import Queue, Process
import time

def process_task(tasks_queue, done_queue, process_no):
    try:
        task_no = tasks_queue.get_nowait()
        time.sleep(0.5)
        print(f'Task no {task_no} is done by Process-{process_no}')
        done_queue.put(task_no)
    except:
        return

num_processes = 4
num_tasks = 10

if __name__ == "__main__":
    tasks_to_accomplish = Queue(10)
    tasks_that_are_done = Queue(10)
    
    for i in range(num_tasks):
        print(f'Task no {i}')
        tasks_to_accomplish.put(i)

    """
    - 같은 Task를 동시에 실행하고, tasks_to_accomplish Queue에서 동시에 get_nowait 실행
    - N번 프로세스가 Queue에서 get을 한 뒤 Queue가 동기화 되기 전 다른 프로세스가 get을 하면, Empty 오류 발생
    - 그래서 프로세스 중간에 Exception이 발생하고, Task를 모두 실행하지 않을 가능성이 존재 (for문 사용할 경우)

    - Queue.empty() 메서드는 100% 신뢰할 수 있는 결과는 아님
    - while 조건으로 바로 넣게 되면, 10번 중 1번 정도 False를 발생시키고 프로세스가 실행되지 않음
    """
    while True:
        processes = []
        for i in range(num_processes):
            if tasks_to_accomplish.empty():
                break
            p = Process(target=process_task, args=(tasks_to_accomplish, tasks_that_are_done, i + 1))
            processes.append(p)

        for p in processes:
            p.start()

        for p in processes:
            p.join()
        
        if tasks_to_accomplish.empty():
            break
