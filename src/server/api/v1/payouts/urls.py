from rest_framework.routers import DefaultRouter

from server.api.v1.payouts.views import PayoutViewSet


router = DefaultRouter()
router.register("payouts", PayoutViewSet, basename="payouts")
