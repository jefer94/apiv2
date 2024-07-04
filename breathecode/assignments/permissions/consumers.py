import logging

from breathecode.admissions.actions import is_no_saas_student_up_to_date_in_any_cohort
from breathecode.authenticate.actions import get_user_language
from breathecode.utils.decorators import PermissionContextType
from breathecode.utils.i18n import translation
from capyc.rest_framework.exceptions import PaymentException

logger = logging.getLogger(__name__)


def code_revision_service(context: PermissionContextType, args: tuple, kwargs: dict) -> tuple[dict, tuple, dict]:
    request = context["request"]
    lang = get_user_language(request)

    if is_no_saas_student_up_to_date_in_any_cohort(context["request"].user) is False:
        raise PaymentException(
            translation(
                lang,
                en="You can't access this asset because your finantial status is not up to date",
                es="No puedes acceder a este recurso porque tu estado financiero no está al dia",
                slug="cohort-user-status-later",
            )
        )

    context["consumables"] = context["consumables"].filter(service_set__slug="code_revision")
    return (context, args, kwargs)
