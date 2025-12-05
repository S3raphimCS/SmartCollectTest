from unittest.mock import patch

import pytest
from django.urls import reverse

from server.apps.payouts.models import Payout, PayoutStatus


@pytest.mark.django_db(transaction=True)
def test_create_payout(client):
    """Проверка создания выплаты"""

    url = reverse("api_v1:payouts-list")
    data = {
        "amount": "100.50",
        "currency": "RUB",
        "recipient_account": "user@example.com",
    }

    # Мокаем вызов задачи Celery, чтобы не запускать реальный воркер в юнит-тестах
    with patch("server.apps.periodic_tasks.tasks.process_payout.delay") as mock_task:
        response = client.post(url, data)

    assert response.status_code == 201
    assert Payout.objects.count() == 1

    payout = Payout.objects.first()
    assert payout.status == PayoutStatus.PENDING
    assert str(payout.amount) == "100.50"

    # Проверяем, что задача Celery была вызвана
    mock_task.assert_called_once_with(payout.id)


@pytest.mark.django_db
def test_create_payout_invalid_amount(client):
    """Проверка создания выплаты с некорректными данными"""

    url = reverse("api_v1:payouts-list")
    data = {
        "amount": "-50.00",
        "currency": "RUB",
        "recipient_account": "user@example.com",
    }
    response = client.post(url, data)
    assert response.status_code == 400
    assert "amount" in response.data
