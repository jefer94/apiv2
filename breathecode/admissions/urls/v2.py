from django.urls import path

from ..views import PublicCohortTimeSlotV2View, PublicCohortUserV2View, PublicCohortV2View
from .v1 import urlpatterns as urlpatterns_v1

deprecation_list = [
    "upload",
]

app_name = "admissions"
urlpatterns = [
    path("public/cohort", PublicCohortV2View.as_view(), name="cohort_all2"),
    path("public/cohort/user", PublicCohortUserV2View.as_view(), name="public_cohort_user2"),
    # path("public/cohort/<int:id>", PublicCohortV2View.as_view(), name="cohort_id"),
    # path("public/cohort/<int:id>/user", PublicCohortUserV2View.as_view(), name="cohort_id_user"),
    path("public/cohort/<int:id>/timeslot", PublicCohortTimeSlotV2View.as_view(), name="cohort_id_timeslot"),
    path("public/cohorttimeslot", PublicCohortTimeSlotV2View.as_view(), name="public_cohorttimeslot"),
    *[r for r in urlpatterns_v1 if r.pattern._route not in deprecation_list],
]
