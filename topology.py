from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, Controller
from mininet.topo import SingleSwitchTopo
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def main():
    net = Mininet(
        topo=SingleSwitchTopo(k=3),
        controller=Controller,
        switch=OVSKernelSwitch,
        autoSetMacs=True
    )

    net.start()

    info("\n*** Network started\n")
    info("*** Hosts: h1 (server), h2 and h3 (agents)\n")

    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    main()
