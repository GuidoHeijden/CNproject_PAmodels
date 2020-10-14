from scipy.stats import bernoulli
import pydot as pyd

# Define edge step functions
def edgeStepFun1(t): # 1/linear function
    return 1 / (t ^ 1.01)

def edgeStepFun2(t): # 1/log-squared function
    return 1 / (np.log(t)**2)

def edgeStepFun3(t): # 1/log-function
    return 1 / log(t)

def main():
    '''
        This function starts asking for input to the user in order to correctly run a
        simulation of the Preferential Attachment models with edgestep function described by
        Alves Ribeiro and Sanchis.
        '''
    delta = float(input('Enter the value of delta\n'))
    m = int(input('Enter the value of m\n'))
    num_iterations = int(input('Enter the number of iterations, i.e. at what t to stop\n'))
    edgestepfunction      = int(input("Which edgestep function do you want to use? (1 | 2 | 3)\n"
                               "---- 0 : 1 / (t ^ 1.01)\n"
                               "---- 1 : 1 / (np.log(t)*2)\n"
                               "---- 2 : 1 / log(t)\n
    # Throw exceptions for incorrect input
    if edgestepfunction < 0 or edgestepfunction > 2:
        raise Exception("Enter a correct value for verbosity!")
    if m < 0:
        raise Exception("m should be greater than zero!")
    if delta < -m:
        raise Exception("delta should be greater or equal to m!\ndelta: " + str(delta) + "\nm: " + str(m))
    if num_iterations < 2:
        raise Exception("There should be at least two iterations!")


    # Run the model with the correct edgestepfunction
    if edgestepfunction == "1":
        G = hofstad_PA_start(m)
        G = model_edgestepfunc(G, delta, m, t=1, t_stop=num_iterations, edgestep=edgeStepFun))
    elif which_model == "2":
        G = hofstad_PA_start(m)
        G = hofstad_PA_b(G, delta, m, t=1, t_stop=num_iterations, edgestep=edgestepFun2)
    elif which_model == "3":
        G = hofstad_PA_start(m)
        G = hofstad_PA_b(G, delta, m, t=1, t_stop=num_iterations, edgestep=edgestepFun3)
    else:
        raise Exception("Enter a correct model version!")

visualisation.display_graph(G)

def model_edgestepfunc(G, delta, m, t, t_stop=10, edgestep=True)

    for t in range (t,t_stop) :
        p=edgestep(t)
        PA_model2(G, m, p, t, t_stop, num_iterations)

    return G

