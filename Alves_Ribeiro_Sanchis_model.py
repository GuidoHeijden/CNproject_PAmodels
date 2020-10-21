from scipy.stats import bernoulli
import pydot as pyd

# Define edge step functions
from Alves_RIbeiro_Sanchis_edge_vertex import PA_model2


def edgeStepFun1(t): # 1/linear function
    return 1 / (t ^ 1.01)

def edgeStepFun2(t): # 1/log-squared function
    return 1 / (np.log(t)**2)

def edgeStepFun3(t): # 1/log-function
    return 1 / log(t)

def model_edgestepfunc(G, delta, m, t, t_stop=10, edgestep=True):
    for t in range (t,t_stop) :
        p=edgestep(t)
        PA_model2(G, m, p, t=1, t_stop)

    return G

