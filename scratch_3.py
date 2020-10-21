import networkx as nx
import random
import scipy
from networkx import utils
import numpy as np

# Choose graph size
n = 5
seq = nx.utils.powerlaw_sequence(n)
print(seq)
for i in range(n):
    G.add_node(i, weight = seq[i])