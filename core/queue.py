import queue
import threading
import uuid
from typing import Callable, Optional
from .reporter import MetaReporter
from .models import ReportData

class ReportJob:
    def __init__(self, report_data: ReportData, chat_id: int, progress_callback=None, completion_callback=None):
        self.id = str(uuid.uuid4())[:8]
        self.report_data = report_data
        self.chat_id = chat_id
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
        self.status = "queued"

class QueueManager:
    def __init__(self):
        self.queue = queue.Queue()
        self.worker_thread = None
        self.is_running = False

    def submit(self, report_data: ReportData, chat_id: int, progress_callback=None, completion_callback=None):
        job = ReportJob(report_data, chat_id, progress_callback, completion_callback)
        self.queue.put(job)
        print(f"[Queue] Job {job.id} submitted | Queue size: {self.queue.qsize()}")
        return job

    def start_worker(self):
        if self.worker_thread and self.worker_thread.is_alive():
            return

        self.is_running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        print("[Queue] Worker started.")

    def _worker(self):
        while self.is_running:
            job = None
            try:
                job = self.queue.get(timeout=1)
                job.status = "running"
                print(f"[Worker] Starting job {job.id}")

                reporter = MetaReporter(
                    report_data=job.report_data,
                    headless=True,
                    progress_callback=job.progress_callback
                )
                reporter.run()

                job.status = "completed"
                if job.completion_callback:
                    job.completion_callback(job, success=True)

            except queue.Empty:
                continue
            except Exception as e:
                print(f"[Worker] Job {job.id if job else 'unknown'} failed: {e}")
                if job:
                    job.status = "failed"
                    if job.completion_callback:
                        job.completion_callback(job, success=False, error=str(e))
            finally:
                if job:
                    self.queue.task_done()

    def stop(self):
        self.is_running = False