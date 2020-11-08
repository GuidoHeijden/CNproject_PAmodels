# CNproject_PAmodels

Welcome to the repository focussed on simulating Preferential Attachment (PA) models/graphs (with edge-steps / edge-step functions)! This repository was created for a project regarding PA models for the course Complex Networks given at the University of Twente. Besides simulating PA models, the aim was also to look at properties of these graphs, specifically the diameter, average distance and typical distance. This repository was updated through PyCharm, and the .idea and venv folders provide functionality for in PyCharm (they include the necessary libraries).

## Description of files & instructions of use
*Important note* : certain functionality regarding visualization required project members to add files to their PATH variables. It might occur that encounter similar problems, which cannot be resolved within this repository. You are able to disable visualization by commenting out any lines of code regarding visualization, or you can search online for any errors presented to you.

PA model simulating files:
- **Hofstad_model.py** includes the functions for simulating models A and B described by Remco Hofstad in his lecture notes "Random Graphs and Complex Networks". These can be regarded as "standard" PA models, where model A can result in a disconnected graph that includes self-loops, while model B does not allow for self-loops, which means that the resulting graph is always connected.
- **Alves_RIbeiro_Sanchis_edge_vertex.py** includes the function for simulating the PA model with edge-steps described by C. Alves, R. Ribeiro and R. Sanchis (2019) "Agglomeration in a Preferenatial Attachment Random Graph with Edge-Steps".
- **Alves_RIbeiro_Sanchis_model.py** includes the function for simulating the PA model with edge-step **functions** described by C. Alves, R. Ribeiro and R. Sanchis (2019) "Topological Properties of P.A. Random Graphs with Edge-Step Functions".

Running simulation and experiments files:
- **choosePAmodel.py** prompts user input to simulate any of the above PA models where the user is also asked for model parameters and the verbosity of the output (only display the last model; also print probability; or display the graph at each iteration). Running this Python file will start the input prompt.
- **distances.py** contains functions for computing the diameter, average distance and simulating the typical distance. There are also some functions for creating figures including these graph properties. Look at the function description of those functions to better understand what they do. Some examples of how to use these functions is given at the bottom of the Python file. Running this file will run the code at the bottom of the file, where you can put any version of a function given in the file.

Additional files:
- **visualisation.py** includes functions for visualizing graphs using the Kamada-Kawai layout. Vertices are colored based on the number of adjacencies, and all vertices and edges in the graph are displayed. It is also possible to view the graph as a DOT file or as a DOT graph.
- **hofstad_PA.dot** the latest graph saved as a DOT file for visualization purposes.

Feel free to email to g.a.m.vanderheijden@student.utwente.nl with any questions regarding this repository (note that this email address is not permanent).
