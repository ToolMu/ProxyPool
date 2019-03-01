from queue import Queue
import threading


StopEvent = object()


class ThreadPool:
    def __init__(self, thread_num=4):
        self._task_queue = Queue(thread_num)
        self._max_thread_num = thread_num
        self._free_thread_queue = []

        for _ in range(thread_num):
            self._create_thread()

    def add(self, func, args, callback=None):
        """
        添加待处理事件 到处理队列中
        """
        self._task_queue.put((func, args, callback,))

    def normal_stop(self):
        """
        停止
        """
        for _ in range(self._max_thread_num):
            self._task_queue.put(StopEvent)

    def status(self):
        free_len = len(self._free_thread_queue)
        return {
            "using": self._max_thread_num - free_len,
            "free": free_len
        }

    def _create_thread(self):
        """
        创建线程： 线程内部决定自己是空闲还是被使用
        """
        new_thread = threading.Thread(target=self._call)
        new_thread.start()

    def _call(self):
        """
        线程工作内容
        """
        thread_name = threading.currentThread()

        event = self._task_queue.get()
        while event != StopEvent:
            func, func_args, callback = event
            try:
                func_result = func(*func_args)
            except Exception as e:
                func_result = None

            if callback:
                try:
                    callback(func_result)
                except Exception as e:
                    pass

            try:
                self._free_thread_queue.append(thread_name)
                event = self._task_queue.get()
            finally:
                self._free_thread_queue.remove(thread_name)


if __name__ == '__main__':
    pool = ThreadPool(3)

    import time

    def callback(status):
        print("OK" if status else "OVER")


    def action(i):
        time.sleep(2)
        print(i)
        return True

    for i in range(30):
        pool.add(action, (i,), callback=callback)

    for _ in range(3):
        print(pool.status())
        time.sleep(2)

    print(pool.status())
    # for i in range(30):
    #     pool.add(action, (i,))
    #
    # print(pool.status())
    pool.normal_stop()
