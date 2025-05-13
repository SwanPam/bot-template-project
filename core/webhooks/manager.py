import time
import requests
from queue import Queue
from threading import Thread

class WebhookManager:
    def __init__(self):
        self.current_url = ""
        self.fallback_urls = []
        self.webhook_queue = Queue()
        self.active = True 
        self.retry_thread = Thread(target=self._process_queue, daemon=True)
        self.retry_thread.start()

    def add_fallback_url(self, url):
        self.fallback_urls.append(url)

    def update_current_url(self, new_url):
        self.current_url = new_url

    def receive_webhook(self, data):
        if not self._send_to_current_url(data):
            self.webhook_queue.put(data)
            return False
        return True

    def _send_to_current_url(self, data):
        try:
            response = requests.post(self.current_url, json=data, timeout=5)
            return response.status_code == 200
        except:
            return False

    def _process_queue(self):
        while self.active:
            if not self.webhook_queue.empty():
                data = self.webhook_queue.get()
                success = self._retry_send(data)
                if not success:
                    self.webhook_queue.put(data)  # Возвращаем в очередь если не удалось
            time.sleep(5)

    def _retry_send(self, data):
        if self._send_to_current_url(data):
            return True
        
        for url in self.fallback_urls:
            try:
                response = requests.post(url, json=data, timeout=5)
                if response.status_code == 200:
                    return True
            except:
                continue
        return False

    def shutdown(self):
        self.active = False
        self.retry_thread.join()