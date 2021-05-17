# import CertificateTimeSlot
import logging
from breathecode.scheduling.models import TaskRules
from datetime import timedelta


logger = logging.getLogger(__name__)


def create_cohort_timeslot(certificate_timeslot, cohort_id):
    from breathecode.admissions.models import CohortTimeSlot
    cohort_timeslot = CohortTimeSlot(
        parent=certificate_timeslot,
        cohort_id=cohort_id,
        starting_at=certificate_timeslot.starting_at,
        ending_at=certificate_timeslot.ending_at,
        recurrent=certificate_timeslot.recurrent,
        recurrency_type=certificate_timeslot.recurrency_type)

    logger.info(f'create timeslot for cohort {cohort_id} based on certificate timeslot {certificate_timeslot.id}')
    cohort_timeslot.save(force_insert=True)


def update_cohort_timeslot(certificate_timeslot, cohort_timeslot):
    is_change = (
        cohort_timeslot.starting_at != certificate_timeslot.starting_at or
        cohort_timeslot.ending_at != certificate_timeslot.ending_at or
        cohort_timeslot.recurrent != certificate_timeslot.recurrent or
        cohort_timeslot.recurrency_type != certificate_timeslot.recurrency_type
    )

    if not is_change:
        logger.info(f'Cohort timeslot {cohort_timeslot.id} is updated')
        return

    cohort_timeslot.starting_at = certificate_timeslot.starting_at
    cohort_timeslot.ending_at = certificate_timeslot.ending_at
    cohort_timeslot.recurrent = certificate_timeslot.recurrent
    cohort_timeslot.recurrency_type = certificate_timeslot.recurrency_type

    logger.info(f'update cohort timeslot {cohort_timeslot.id} based on certificate timeslot {certificate_timeslot.id}')
    cohort_timeslot.save()


def create_or_update_cohort_timeslot(certificate_timeslot):
    from breathecode.admissions.models import Cohort, CohortTimeSlot

    cohort_ids = Cohort.objects.filter(
        syllabus__certificate__id=certificate_timeslot.certificate.id)\
            .values_list('id', flat=True)

    for cohort_id in cohort_ids:
        cohort_timeslot = CohortTimeSlot.objects.filter(
            parent__id=certificate_timeslot.id,
            cohort__id=cohort_id).first()

        if cohort_timeslot:
            update_cohort_timeslot(certificate_timeslot, cohort_timeslot)

        else:
            create_cohort_timeslot(certificate_timeslot, cohort_id)

logger.info(f'Syncing cohort timeslots')

if not TaskRules.objects.filter(slug='sync-cohort-timeslots', frequency_delta=timedelta(hours=3)).exists():
    task = TaskRules.objects.filter(slug='sync-cohort-timeslots')
    task.frequency_delta = timedelta(hours=3)
    task.save()

certificate_timeslots = CertificateTimeSlot.objects.filter()

for certificate_timeslot in certificate_timeslots:
    create_or_update_cohort_timeslot(certificate_timeslot)

logger.info(f'Done!')
