from .testbed import Simulation
from .methods import Act
from .scenarios import HostileEnvironment, StartLying
import matplotlib.pyplot as plt

scenario = StartLying(
    witness_amount=5,
    consumer_amount=5,
    provider_amount=20,
    provider_options={"chance": 0.7, "l_quality": 0.8, "l_cost": 0.3, "u_cost": 0.6},
)

ntcm = Act
sim = Simulation(scenario, ntcm, 1000)


for c, p in sim.runs(4):
    print()
    print(f"Consumer Average: {sum(sum(c[_c]) for _c in c )/len(c):.2f}")
    print(f"Provider Average: {sum(sum(p[_p]) for _p in p)/len(p):.2f}")
    c_list = {_c: [sum(_v[:v]) for v in range(len(_v))] for _c, _v in c.items()}
    best_c = max(c_list.keys(), key=lambda c: c_list[c][-1])
    p_list = {_p: [sum(_v[:v]) for v in range(len(_v))] for _p, _v in p.items()}
    best_p = max(p_list.keys(), key=lambda p: p_list[p][-1])
    c_label_set = False
    p_label_set = False
    average_p = [sum(x) / len(p_list.values()) for x in zip(*p_list.values())]
    average_c = [sum(x) / len(c_list.values()) for x in zip(*c_list.values())]
    plt.plot(average_c, "-", linewidth=4, label="Average Consumer")
    plt.plot(average_p, ":", linewidth=4, label="Average Provider")

    for _c in c:
        if best_c == _c:
            plt.plot(c_list[_c], "-b", label="Best Consumer")
        else:
            if not c_label_set:
                plt.plot(c_list[_c], "-g", label="Consumer")
                c_label_set = True
            else:
                plt.plot(c_list[_c], "-g")
    for _p in p:
        if best_p == _p:
            plt.plot(p_list[_p], ":c", label="Best Provider")
        else:
            if not p_label_set:
                plt.plot(p_list[_p], ":r", label="Provider")
                p_label_set = True
            else:
                plt.plot(p_list[_p], ":r")
    plt.title("Trust Simulation")
    plt.xlabel("Time step")
    plt.ylabel("Utility")
    plt.legend()
    plt.show()
