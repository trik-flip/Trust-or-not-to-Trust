from time import time_ns


class ToDoException(Exception):
    def __str__(self):
        return f"This method is not implemented!"


def log(func):
    def new_func(*args, **kwargs):
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
        self.timers = {}

    def switch(self, name1, name2):
        self.stop(name1)
        self.start(name2)

    def start(self, name="main"):
        if name not in self.timers:
            self.timers[name] = {"start": [], "stop": [], "hits": 0}

        self.timers[name]["start"] += [time_ns()]

    def stop(self, name="main"):
        if name not in self.timers:
            raise Exception(f"{name} is not a valid timer")

        self.timers[name]["stop"] += [time_ns()]
        self.timers[name]["hits"] += 1

    def total_time(self, name="main"):
        if name not in self.timers:
            raise Exception(f"{name} is not a valid timer")

        if len(self.timers[name]["start"]) != self.timers[name]["hits"]:
            print(f"[WARNING] - {name} timer is not stopped")
            return 0

        total = 0
        for start, stop in zip(self.timers[name]["start"], self.timers[name]["stop"]):
            total += stop - start
        return total

    def profile(self, func):

        name = f"Function:{func.__name__}"

        def new_func(*args, **kwargs):
            self.start(name)
            result = func(*args, **kwargs)
            self.stop(name)
            return result
        return new_func

    def result(self):
        all_times = list(self.funcs.items())
        for _f, v in all_times:
            v["time per call"] = "not called" if v["hits"] == 0 else v["time"]/v["hits"]
        return sorted(all_times, key=lambda x: x[1]["time"], reverse=True)

    def show(self, zero_runners=True, min_time=0):

        print("\n", "="*100, "\n")
        self.print_manual_timers(zero_runners, min_time)
        print("\n", "="*100, "\n")

    def print_manual_timers(self, zero_runners, min_time):
        if len(self.timers) == 0:
            return
        longest_key = max(len(str(k)) for k in self.timers)
        print(
            f"[Timer]{' '*(longest_key-7)}\t|\t[time]  \t|\t[hit counts]\t|\t[time per call]")
        for timer in sorted(self.timers, key=lambda x: self.total_time(x), reverse=True):
            tt = self.total_time(timer)
            ftt = format_time(tt)
            hc = self.timers[timer]["hits"]
            tpc = "not called" if self.timers[timer]["hits"] == 0 else format_time(
                tt/hc)

            if not zero_runners and hc == 0:
                continue
            if tt/hc < min_time:
                continue
            print(f"{timer:{max(longest_key,7)}}\t|\t{ftt:8}\t|\t{hc:12}\t|\t{tpc}")


def format_time(x):
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
