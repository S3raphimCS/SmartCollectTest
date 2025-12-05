from django_filters import rest_framework as filters

from server.apps.payouts.enums import PayoutStatus
from server.apps.payouts.models import Payout


class PayoutFilterSet(filters.FilterSet):
    """Фильтр выплат."""

    min_amount = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr="lte")

    currency = filters.CharFilter(lookup_expr="iexact")
    status = filters.ChoiceFilter(choices=PayoutStatus.choices)

    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Payout
        fields = ["recipient_account", "currency", "status"]
