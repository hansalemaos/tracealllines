import inspect
import os
import sys
from functools import lru_cache, wraps

colex = sys.modules[__name__]
colex.allcolors = {}
colex.allcolors["black"] = "\033[30m"
colex.allcolors["red"] = "\033[31m"
colex.allcolors["green"] = "\033[32m"
colex.allcolors["orange"] = "\033[33m"
colex.allcolors["blue"] = "\033[34m"
colex.allcolors["purple"] = "\033[35m"
colex.allcolors["cyan"] = "\033[36m"
colex.allcolors["lightgrey"] = "\033[37m"
colex.allcolors["darkgrey"] = "\033[90m"
colex.allcolors["lightred"] = "\033[91m"
colex.allcolors["lightgreen"] = "\033[92m"
colex.allcolors["yellow"] = "\033[93m"
colex.allcolors["lightblue"] = "\033[94m"
colex.allcolors["pink"] = "\033[95m"

colex.file = None
colex.colo = None
colex.logfile = None
c_reset = "\033[0m"


def touch(path: str) -> bool:
    def _fullpath(path):
        return os.path.abspath(os.path.expanduser(path))

    def _mkdir(path):
        path = path.replace("\\", "/")
        if path.find("/") > 0 and not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

    def _utime(path):
        try:
            os.utime(path, None)
        except Exception:
            open(path, "a").close()

    def touch_(path):
        if path:
            path = _fullpath(path)
            _mkdir(path)
            _utime(path)

    try:
        touch_(path)
        return True
    except Exception as Fe:
        print(Fe)
        return False


def pc(text, color):
    text = str(text)
    return f"{color}{text}{c_reset}"


def tracefunction(frame, event, arg):
    try:
        file, color, logfile = colex.file, colex.colo, colex.logfile
        info = inspect.getframeinfo(frame)
        fname, lineno, fn = info.filename, info.lineno, info.function
        if fname == file:
            line = read_fi(fname, lineno)
            tra = lineno, repr(line)[2:-1]
            if color:
                col = pc(text=f"{str(tra[0]).ljust(6)}:\t{tra[1]}", color=color)
                print(col)
            if logfile:
                if not os.path.exists(logfile):
                    touch(logfile)
                with open(logfile, mode="a", encoding="utf-8") as f:
                    f.write(f"{str(tra[0]).ljust(6)}:\t{tra[1]}\n")
        return tracefunction
    except Exception as fe:
        print(fe)
        return tracefunction


def print_execution(f_py=None, file=None, color=None, logfile=None, enabled=True):
    assert callable(f_py) or f_py is None

    colex.file = file
    colex.colo = colex.allcolors[color]
    colex.logfile = logfile

    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if enabled:
                    sys.settrace(tracefunction)
                vala = func(*args, **kwargs)
            except Exception as fe:
                sys.settrace(None)
                raise fe
            finally:
                sys.settrace(None)

            return vala

        return wrapper

    return _decorator(f_py) if callable(f_py) else _decorator


@lru_cache
def read_fi(fname, lineno):
    try:
        with open(fname, "rb") as f:
            line = [line.rstrip() for line in f][lineno - 1]
    except Exception:
        return f"ERROR OPENING {fname}"
    return line


def enable_trace_all(file, color, logfile):
    colex.file = file
    colex.colo = colex.allcolors[color]
    colex.logfile = logfile
    sys.settrace(tracefunction)


def disable_trace_all():
    sys.settrace(None)
