from rest_framework import serializers

from server.apps.payouts.models import Payout


class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = [
            "id",
            "amount",
            "currency",
            "recipient_account",
            "status",
            "description",
            "error_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "error_message", "created_at", "updated_at"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма выплат должна быть больше нуля.")
        return value
