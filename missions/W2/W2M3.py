from multiprocessing import Queue

num_items = 4

def push(itmes, queue):
    print('pushing items to queue:')
    for i in range(num_items):
        queue.put(items[i])
        print(f'item no: {i + 1} {items[i]}')

def pop(queue):
    print('popping items from queue:')
    i = 0
    while not queue.empty():
        print(f'item no: {i} {queue.get()}')
        i += 1

if __name__ == "__main__":
    queue = Queue(10)
    items = ['red', 'green', 'blue', 'black']
    push(items, queue)
    pop(queue)