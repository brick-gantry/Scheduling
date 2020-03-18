from src.tasks.execution import execute_task
from io import StringIO


def test_execute_task():
    stdout = StringIO()
    execute_task('echo hello world', stdout=stdout)
    stdout.seek(0)
    assert stdout.read().strip() == 'hello world'
