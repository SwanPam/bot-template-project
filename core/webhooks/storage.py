import json
from typing import List, Tuple, Optional
from sqlalchemy import func, select, update, delete
from database.engine import async_session
from database.models import FailedWebhook

class WebhookStorage:
    async def store_failed(self, payload: dict, original_url: str) -> Optional[int]:
        """
        Сохраняет неотправленный вебхук в базу данных
        
        :param payload: Данные вебхука (словарь)
        :param original_url: Оригинальный URL назначения
        :return: ID сохраненной записи или None при ошибке
        """
        async with async_session() as session:
            try:
                payload_str = json.dumps(payload, ensure_ascii=False)
                new_failed_webhook = FailedWebhook(
                    payload=payload_str,
                    original_url=original_url
                )
                session.add(new_failed_webhook)
                await session.commit()
                await session.refresh(new_failed_webhook)
                return new_failed_webhook.id
            except Exception as e:
                await session.rollback()
                print(f"Error storing failed webhook: {str(e)}")
                return None

    async def get_pending_webhooks(self, limit: int = 100) -> List[Tuple[int, dict]]:
        """
        Получает список вебхуков для повторной отправки
        
        :param limit: Максимальное количество вебхуков
        :return: Список кортежей (id, payload)
        """
        async with async_session() as session:
            try:
                result = await session.execute(
                    select(FailedWebhook.id, FailedWebhook.payload)
                    .where(FailedWebhook.retry_count < 5)
                    .order_by(FailedWebhook.received_at)
                    .limit(limit)
                )
                webhooks = []
                for id, payload_str in result.all():
                    try:
                        payload = json.loads(payload_str)
                        webhooks.append((id, payload))
                    except json.JSONDecodeError:
                        continue
                return webhooks
            except Exception as e:
                print(f"Error fetching pending webhooks: {str(e)}")
                return []

    async def mark_retry(self, webhook_id: int, success: bool) -> bool:
        """
        Обновляет статус вебхука после попытки отправки
        
        :param webhook_id: ID вебхука
        :param success: Успешность отправки
        :return: Статус выполнения операции
        """
        async with async_session() as session:
            try:
                if success:
                    await session.execute(
                        delete(FailedWebhook)
                        .where(FailedWebhook.id == webhook_id)
                    )
                else:
                    await session.execute(
                        update(FailedWebhook)
                        .where(FailedWebhook.id == webhook_id)
                        .values(
                            retry_count=FailedWebhook.retry_count + 1,
                            last_retry=func.now()
                        )
                    )
                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                print(f"Error updating webhook {webhook_id}: {str(e)}")
                return False