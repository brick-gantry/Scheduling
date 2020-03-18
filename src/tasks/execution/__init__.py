import subprocess
import sys
import threading


def _default_subprocess_reader(proc_stream, local_stream):
    for line in iter(proc_stream.readline, b''):
        local_stream.write(line.decode('utf-8'))


def execute_task(task_phrase, stdout=None, stderr=None):
    proc = subprocess.Popen(task_phrase, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout_t = threading.Thread(target=_default_subprocess_reader, args=(proc.stdout, stdout or sys.stdout))
    stderr_t = threading.Thread(target=_default_subprocess_reader, args=(proc.stderr, stderr or sys.stderr))
    stdout_t.start()
    stderr_t.start()
    stdout_t.join()
    stderr_t.join()