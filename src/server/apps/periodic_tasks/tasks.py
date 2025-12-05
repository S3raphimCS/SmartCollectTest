import time

from django.db import transaction
from loguru import logger

from server import celery_app
from server.apps.payouts.enums import PayoutStatus
from server.apps.payouts.models import Payout


@celery_app.app.task
def process_payout(payout_id: int) -> None:
    """Имитирует работу со сторонним сервисом выплат"""

    logger.info(f"Обработка выплаты №{payout_id}")
    try:
        with transaction.atomic():
            payout = Payout.objects.select_for_update().get(id=payout_id)

            if payout.status != PayoutStatus.PENDING:
                logger.warning(
                    f"Выплата №{payout_id} имеет статус отличный от 'В ожидании' . Текущий статус: {payout.status}"
                )
                return

            payout.status = PayoutStatus.PROCESSING
            payout.save()

        time.sleep(5)

        payout.status = PayoutStatus.COMPLETED
        payout.save()
        logger.info(f"Выплата №{payout_id} успешно завершена.")

    except Payout.DoesNotExist:
        logger.error(f"Выплата №{payout_id} не найдена.")

    except Exception as err:
        logger.error(f"Ошибка при обработке выплаты №{payout_id}: {err}")
        try:
            payout = Payout.objects.get(id=payout_id)
            payout.status = PayoutStatus.FAILED
            payout.error_message = str(err)[:1000]  # Обрезаем, если слишком длинная
            payout.save()
        except Exception as exc:
            logger.error(
                f"Ошибка при обновлении статуса выплаты №{payout_id} на 'Ошибка': {exc}"
            )
