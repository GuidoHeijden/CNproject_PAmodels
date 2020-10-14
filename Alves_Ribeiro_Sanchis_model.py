from scipy.stats import bernoulli
import pydot as pyd

# Define edge step functions
def edgeStepFun1(t): # 1/linear function
    return 1 / (t ^ 1.01)

def edgeStepFun2(t): # 1/log-squared function
    return 1 / (np.log(t)**2)

def edgeStepFun3(t): # 1/log-function
    return 1 / log(t)