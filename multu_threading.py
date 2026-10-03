import threading
import time


def download_file():
    print("downloading file",sep="\n")
    time.sleep(5)
    print("current thread",threading.current_thread(),sep="")
    print("downloaded file")

def read_file():
    print("reading file")
    time.sleep(5)
    print("read file")


t1=threading.Thread(target=download_file)
t1.start()

t1.join()
read_file()

