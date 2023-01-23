from to_trust.agents.consumer import Consumer

from .metrics import MetricSystem


@MetricSystem.register("MAE")
def MAE(consumers: dict[Consumer, float], providers, epochs):
    T = epochs
    N = len(consumers)
    total = 0.0

    for i in range(epochs):
        for c in consumers:
            total += (consumers[c][i] - g(min, providers, epochs)[i]) / (
                g(max, providers, epochs)[i] - g(min, providers, epochs)[i]
            )
    sigma = total / (T * N)
    return 1 - sigma


def g(func, providers, epochs) -> list[float]:
    vals = []
    for i in range(epochs):
        val = 1 if func == min else -1
        for p in providers:
            val = func(providers[p][i], val)
        vals.append(val)
    return vals
