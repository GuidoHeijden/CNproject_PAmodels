import visualisation
from Alves_RIbeiro_Sanchis_edge_vertex import PA_model2
from Alves_Ribeiro_Sanchis_model import model_edgestepfunc, edgeStepFun1, edgeStepFun2, edgeStepFun3
from Hofstad_model import hofstad_PA_start, hofstad_PA, hofstad_PA_start_b, hofstad_PA_b


def choosePAmodel():
    '''
    This function allows for user input to simulate one of the following models:
    - Hofstad model A (see Hofstad_model.py)
    - Hofstad model B (see Hofstad_model.py)
    - Alves Ribereiro Sanchis - PA model with edge steps (see Alves_RIbeiro_Sanchis_edge_vertex.py)
    - Alves Ribereiro Sanchis - PA model with edge-step function (see Alves_RIbeiro_Sanchis_model.py)
    See the python files references behind each of the models above to view the implementation of each
    model and a description.

    :return:
    '''

    whichPA = int(input("Which PA model do you want to use? (0 | 1 | 2)\n"
                               "---- 0 : The PA model by Hofstad\n"
                               "---- 1 : The PA model with edge-step\n"
                               "---- 2 : The PA model with edge-step function\n"))
    delta          = float(input('Enter the value of delta\n'))
    m              = int(input('Enter the value of m\n'))
    num_iterations = int(input('Enter the number of iterations, i.e. at what t to stop\n'))
    verbosity      = int(input("How verbose do you want the simulation to be? (0 | 1 | 2)\n"
                               "---- 0 : only show and save final graph\n"
                               "---- 1 : show probability distribution and selected vertices per iteration\n"
                               "---- 2 : show graph on each iteration (1.5 second breaks between iterations)\n"))
    # Throw exceptions for incorrect input
    if verbosity < 0 or verbosity > 2:
        raise Exception("Enter a correct value for verbosity!")
    if m < 0:
        raise Exception("m should be greater than zero!")
    if delta < -m:
        raise Exception("delta should be greater or equal to m!\ndelta: " + str(delta) + "\nm: " + str(m))
    if num_iterations < 2:
        raise Exception("There should be at least two iterations!")
    if whichPA < 0 or whichPA > 2:
        raise Exception("Enter a correct value for PA model!")

    # Run the correct PA model
    if whichPA == 0:
        which_model = str(input('Which Hofstad model do you want to use? (a | b)\n'))
        if which_model == "a":
            G = hofstad_PA_start(m)
            G = hofstad_PA(G, delta, m, t=1, t_stop=num_iterations, verbose=verbosity)
        elif which_model == "b":
            G = hofstad_PA_start_b(m)
            G = hofstad_PA_b(G, delta, m, t=2, t_stop=num_iterations, verbose=verbosity)
        else:
            raise Exception("Enter a correct model version!")

    elif whichPA == 1:
        p = float(input('Enter the value of probability of choosing an vertex-step\n'))
        if p <= 0 or p >= 1:
            raise Exception("Enter a correct value for p between 0 and 1!")
        G = hofstad_PA_start_b(m)
        G = PA_model2(G, m, p, t=2, t_stop=num_iterations, verbose=verbosity)

    elif whichPA == 2:
        edgestepfunction = int(input("Which edgestep function do you want to use? (1 | 2 | 3)\n"
                                     "---- 0 : 1 / (t^1.01)\n"
                                     "---- 1 : 1 / (log(t)^2)\n"
                                     "---- 2 : 1 / log(t)\n "))
        # Throw exceptions for incorrect input
        if edgestepfunction < 0 or edgestepfunction > 2:
            raise Exception("Enter a correct value for edgestepfunction!")

        # Run the model with the correct edgestepfunction
        if edgestepfunction == 0:
            G = hofstad_PA_start_b(m)
            G = model_edgestepfunc(G, m, edgeStepFun1, t=2, t_stop=num_iterations, verbose=verbosity)
        elif edgestepfunction == 1:
            G = hofstad_PA_start_b(m)
            G = model_edgestepfunc(G, m, edgeStepFun2, t=2, t_stop=num_iterations, verbose=verbosity)
        elif edgestepfunction == 2:
            G = hofstad_PA_start_b(m)
            G = model_edgestepfunc(G, m, edgeStepFun3, t=2, t_stop=num_iterations, verbose=verbosity)
        else:
            raise Exception("Enter a correct model version!")
    else:
        raise Exception("Enter a correct model version!")
    visualisation.display_graph(G)

# To run this model, uncomment the following:

choosePAmodel()

visualisation.visualise_dot()
