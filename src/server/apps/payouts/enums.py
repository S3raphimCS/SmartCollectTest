from django.db import models


class PayoutStatus(models.TextChoices):
    """Статусы выплат."""

    PENDING = "pending", "В ожидании"
    PROCESSING = "processing", "В обработке"
    COMPLETED = "completed", "Завершено"
    FAILED = "failed", "Ошибка"
