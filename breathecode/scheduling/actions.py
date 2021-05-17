import logging, os, sys, contextlib
from django.utils import timezone
from io import StringIO


logger = logging.getLogger(__name__)
USER_AGENT = "BreathecodeMonitoring/1.0"
SCRIPT_HEADER = """
# from django.conf import settings
# import breathecode.settings as app_settings

# settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)

# import django
# django.setup()
"""


def list_tasks():
    root, dirs, files = os.walk(".")
    return [file.replace('_', '-') for file in files if file.endswith(".py")]


def run_task(task):
    @contextlib.contextmanager
    def stdoutIO(stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        header = SCRIPT_HEADER
        content = header + \
            open(f"{dir_path}/scripts/{task.slug.replace('-', '_')}.py").read()

        with stdoutIO() as s:
            try:
                exec(content)

                task.status = 'DONE'
                task.status_text = None

            except Exception as e:
                error = str(e)

                task.status = 'MINOR'
                task.status_text = error

                logger.error(error)

    except FileNotFoundError:
        task.status = 'CRITICAL'
        task.status_text = f"Task not found: {task.slug}"

    except Exception as e:
        error = str(e)
        task.status = 'CRITICAL'
        task.status_text = error

    task.last_run = timezone.now()
    task.save()
