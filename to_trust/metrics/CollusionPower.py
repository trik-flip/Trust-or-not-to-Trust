from .metrics import MetricSystem


@MetricSystem.register("Collusion Power")
def collusion_power(consumers: dict, providers, epochs):
    pass
