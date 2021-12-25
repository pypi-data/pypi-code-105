import threading
import traceback
import time
import sqlq


class base_worker(object):
    terminate = False
    terminated = False
    exploded = False
    exploded_reason = None
    app_root = None
    cookies_domain = None
    sql = None
    writer = None
    export_functions = None
    invert_worker = False
    under_maintenance = False
    maintenance_job_done = False

    def job(self) -> None:
        return

    def _job(self) -> None:
        return self.job()

    def worker(self) -> None:
        while not self.terminate:
            try:
                under_maintenance = self.under_maintenance
                if self.invert_worker:
                    under_maintenance = not under_maintenance
                    if under_maintenance:
                        self.maintenance_job_done = False
                if under_maintenance or self.maintenance_job_done:
                    time.sleep(5)
                    continue
                self._job()
                if self.invert_worker and not under_maintenance:
                    self.maintenance_job_done = True
            except:
                self.exploded_reason = traceback.format_exc()
                self.exploded = True
                break
        self.terminated = True

    def stop(self) -> None:
        self.terminate = True
        while not self.terminated:
            time.sleep(1 / 1000)

    def start(self) -> None:
        p = threading.Thread(target=self.worker)
        p.daemon = True
        p.start()


class once_base_worker(base_worker):
    completed = False

    def _job(self) -> None:
        if not self.completed:
            self.job()
            self.completed = True


class inverted_base_worker(base_worker):
    invert_worker = True


class once_inverted_base_worker(once_base_worker, inverted_base_worker):
    pass


