from django.urls import include, path

from server.api.v1.payouts.urls import router as payout_router


urlpatterns = [
    path("payouts/", include(payout_router.urls)),
]
