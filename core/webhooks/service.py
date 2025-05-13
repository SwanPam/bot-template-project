import asyncio
from core.webhooks.manager import WebhookManager
from core.webhooks.storage import WebhookStorage

class WebhookService:
    def __init__(self):
        self.storage = WebhookStorage()
        self.manager = WebhookManager()
        self.retry_interval = 60  # seconds
        self.active = True
        self.retry_task = None

    async def start(self):
        """Запускает фоновую задачу при старте приложения"""
        self.retry_task = asyncio.create_task(self._retry_failed_webhooks())

    async def stop(self):
        """Останавливает фоновую задачу при завершении"""
        self.active = False
        if self.retry_task:
            self.retry_task.cancel()
            try:
                await self.retry_task
            except asyncio.CancelledError:
                pass

    async def receive_webhook(self, data):
        if not await self.manager.receive_webhook(data):
            await self.storage.store_failed(data, self.manager.current_url)

    async def _retry_failed_webhooks(self):
        while self.active:
            try:
                pending = await self.storage.get_pending_webhooks()
                for webhook_id, payload in pending:
                    success = await self.manager._retry_send(payload)
                    await self.storage.mark_retry(webhook_id, success)
                await asyncio.sleep(self.retry_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in retry loop: {str(e)}")
                await asyncio.sleep(5)  # Задержка при ошибках

    def update_endpoint(self, new_url):
        old_url = self.manager.current_url
        self.manager.add_fallback_url(old_url)
        self.manager.update_current_url(new_url)