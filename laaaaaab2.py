import random 
import time
import asyncio
import matplotlib.pyplot as plt
import networkx as nx

from node import Node, Router
from protocols import UDPProtocol, TCPProtocol
from network import Network

def visualize(network):
    G = nx.Graph()
    for node in network.nodes:
        for conn in node.connections:
            G.add_edge(node.name, conn.name)

    plt.figure(figsize=(6,6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray")
    plt.show()

async def main():
    # Зірка
    star_net = Network()
    center = Router("Switch")
    star_net.nodes.append(center)
    for i in range(5):
        node = Node(f"PC{i}")
        star_net.nodes.append(node)
        center.connect(node)

    print("=== Зірка (TCP) ===")
    await star_net.simulate(TCPProtocol, packets=20)
    star_net.analyze()
    visualize(star_net)

    # Дерево
    tree_net = Network()
    root = Router("Server")
    tree_net.nodes.append(root)
    for i in range(1,3):
        child = Node(f"Switch{i}")
        tree_net.nodes.append(child)
        root.connect(child)
        for j in range(2):
            leaf = Node(f"PC{i}{j}")
            tree_net.nodes.append(leaf)
            child.connect(leaf)

    print("\n=== Дерево (UDP) ===")
    await tree_net.simulate(UDPProtocol, packets=20)
    tree_net.analyze()
    visualize(tree_net)

asyncio.run(main())
