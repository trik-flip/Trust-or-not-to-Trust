from time import time_ns
from typing import Any, Callable


class Singleton(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args: Any, **kwargs: dict[str, Any]):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ToDoException(Exception):
    def __str__(self):
        return f"This method is not implemented!"


def log(func: Callable[[Any], Any]):
    def new_func(*args: Any, **kwargs: dict[str, Any]):
        print(f"[Running] - {func}")
        return func(*args, **kwargs)

    return new_func


class Profiler:
    s = 1_000_000_000
    ms = 1_000_000
    us = 1_000
    ns = 1

    def __init__(self) -> None:
        self.funcs = {}
        self.timers: dict[str, dict[str, list[int] | int]] = {}

    def switch(self, name1: str, name2: str):
        self.stop(name1)
        self.start(name2)

    def start(self, name: str = "main"):
        if name not in self.timers:
            self.timers[name] = {"start": [], "stop": [], "hits": 0}

        self.timers[name]["start"] += [time_ns()]  # type: ignore

    def stop(self, name: str = "main"):
        if name not in self.timers:
            raise Exception(f"{name} is not a valid timer")

        self.timers[name]["stop"] += [time_ns()]  # type: ignore
        self.timers[name]["hits"] += 1  # type: ignore

    def total_time(self, name: str = "main") -> int:
        if name not in self.timers:
            raise Exception(f"{name} is not a valid timer")

        if len(self.timers[name]["start"]) != self.timers[name]["hits"]:  # type: ignore
            print(f"[WARNING] - {name} timer is not stopped")
            return 0

        total = 0
        for start, stop in zip(self.timers[name]["start"], self.timers[name]["stop"]):  # type: ignore
            total += stop - start  # type: ignore
        return total  # type: ignore

    def profile(self, func: Callable[[Any], Any]):

        name = f"Function:{func.__name__}"
        self.timers[name] = {"start": [], "stop": [], "hits": 0}

        def new_func(*args: Any, **kwargs: dict[str, Any]):
            self.start(name)
            result = func(*args, **kwargs)
            self.stop(name)
            return result

        return new_func

    def result(self):
        all_times: list[tuple[Any, Any]] = list(self.funcs.items())  # type: ignore
        for _f, v in all_times:
            v["time per call"] = (
                "not called" if v["hits"] == 0 else v["time"] / v["hits"]
            )
        return sorted(all_times, key=lambda x: x[1]["time"], reverse=True)

    def show(self, zero_runners: bool = True, min_time: int = 0):

        print("\n", "=" * 100, "\n")
        self.print_manual_timers(zero_runners, min_time)
        print("\n", "=" * 100, "\n")

    def print_manual_timers(self, zero_runners: bool, min_time: int):
        if len(self.timers) == 0:
            return
        longest_key = max(len(str(k)) for k in self.timers)
        print(
            f"[Timer]{' '*(longest_key-7)}\t|\t[time]  \t|\t[hit counts]\t|\t[time per call]"
        )
        for timer in sorted(
            self.timers, key=lambda x: self.total_time(x), reverse=True
        ):
            tt = self.total_time(timer)
            ftt = format_time(tt)
            hc = self.timers[timer]["hits"]
            tpc = (
                "not called"
                if self.timers[timer]["hits"] == 0
                else format_time(tt / hc)  # type: ignore
            )

            if not zero_runners and hc == 0:
                continue
            if min_time != 0 and (hc == 0 or tt / hc < min_time):  # type: ignore
                continue
            print(f"{timer:{max(longest_key,7)}}\t|\t{ftt:8}\t|\t{hc:12}\t|\t{tpc}")


def format_time(x: int):
    if isinstance(x, str):
        return x
    if x > 1_000_000_000:
        return f"{x/1_000_000_000:.2f}s"
    if x > 1_000_000:
        return f"{x/1_000_000:.2f}ms"
    if x > 1_000:
        return f"{x/1_000:.2f}us"
    return f"{x:.2f}ns"


profiler = Profiler()
