from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from server.api.v1.payouts.filters import PayoutFilterSet
from server.api.v1.payouts.serializers import PayoutSerializer
from server.apps.payouts.models import Payout
from server.apps.periodic_tasks.tasks import process_payout


class PayoutViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Payout."""

    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = PayoutFilterSet
    search_fields = ["recipient_account", "description"]
    ordering_fields = ["created_at", "amount", "status"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        """Создание объекта Payout с отправкой задачи в очередь."""
        instance = serializer.save()

        transaction.on_commit(lambda: process_payout.delay(instance.id))

    @swagger_auto_schema(
        operation_description="""
        Получение списка выплат. Возможные фильтры:
        currency - Валюта.
        status - Статус выплаты. Возможные значение: pending, processing, completed, failed
        Диапазоны - amount (min_amount, max_amount) и created (created_after, created_before)
        Поиск по полям: recipient_account, description.
        Сортировка по полям: created_at, amount, status.
        """,
        operation_summary="Список выплат с фильтрацией.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получение выплаты по id.",
        operation_summary="Получение выплаты по id.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание выплаты.", operation_summary="Создание выплаты."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удаление выплаты.", operation_summary="Удаление выплаты."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновление выплаты.",
        operation_summary="Обновление выплаты.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частичное обновление выплаты.",
        operation_summary="Частичное обновление выплаты.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
