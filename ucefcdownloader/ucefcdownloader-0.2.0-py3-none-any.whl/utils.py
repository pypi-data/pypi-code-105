import threading
import traceback


class ThreadWrapper:
    def __init__(self, semaphore: threading.Semaphore) -> None:
        self.total_thread_count = 0
        self.threads = []
        self.sema = semaphore
        self.debug_time = False

    def __run_job(self, job, result = None, key = None) -> None:
        response = None
        try:
            self.sema.acquire()
            self.total_thread_count += 1
            response = job()
            if isinstance(result, list):
                result.append(response)
            elif isinstance(result, dict):
                result[key] = response
        except:
            response = traceback.format_exc()
        finally:
            self.sema.release()
            return response

    def add(self, *, job, result = None, key = None) -> bool:
        if result is None:
            result = {}
        if key is None:
            key = 0
        thread = threading.Thread(target=self.__run_job, args=(job, result, key))
        self.threads.append(thread)
        thread.start()
        return True

    def wait(self) -> bool:
        for thread in self.threads:
            thread.join()
        return True



