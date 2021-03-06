import logging
from breathecode.services.google_cloud import Storage

BUCKET_NAME = "admissions-breathecode"
logger = logging.getLogger(__name__)

def get_bucket_object(file_name):
    if not file_name:
        return False

    storage = Storage()
    file = storage.file(BUCKET_NAME, file_name)
    return file.blob