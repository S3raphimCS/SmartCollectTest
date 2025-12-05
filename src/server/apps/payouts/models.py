import uuid

from django.db import models

from server.apps.payouts.enums import PayoutStatus


class Payout(models.Model):
    """Модель выплат"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(
        verbose_name="Сумма для выплат", max_digits=12, decimal_places=2
    )
    currency = models.CharField(
        verbose_name="ISO 4217 Код валюты", max_length=3, default="RUB"
    )
    recipient_account = models.CharField(
        verbose_name="Кошелек получателя", max_length=100
    )
    status = models.CharField(
        verbose_name="Статус выплаты",
        max_length=20,
        choices=PayoutStatus.choices,
        default=PayoutStatus.PENDING,
        db_index=True,
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    error_message = models.TextField(verbose_name="Текст ошибки", blank=True, null=True)

    created_at = models.DateTimeField(
        verbose_name="Дата и время создания", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата и время изменения", auto_now=True
    )

    class Meta:
        verbose_name = "Выплата"
        verbose_name_plural = "Выплаты"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} - {self.amount} {self.currency} ({self.status})"
