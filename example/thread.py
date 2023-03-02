import threading
import time

def thread_1():
    for i in range(10):
        print("Thread 1")
        time.sleep(1)

def thread_2():
    for i in range(10):
        print("Thread 2")
        time.sleep(1)

thread1 = threading.Thread(target=thread_1)
thread2 = threading.Thread(target=thread_2)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
