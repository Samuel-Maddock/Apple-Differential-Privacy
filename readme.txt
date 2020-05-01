# ---------- Installation -------------

To install dependencies for the project when in the root directory run:
    python -m pip install -r ./requirements.txt

# --------------- Structure of Code ------------------

All the code for the algorithms are under the algorithms module:
    1) apple_ldp - Implementations of CMS, HCMS and SFP
    2) bnst_ldp - Implementations of TreeHistogram, Private Count Sketch, Hashtogram, SuccinctHist, ExplicitHist, Bitstogram
    3) RAPPOR -  Python 3 implementation and wrapper of Google's RAPPOR (client + server side)

All of the simulation framework code is within the simulation module:
    1) frequency_oracles - Store wrappers and helpers for all the frequency oracle algorithms, and store code for the Normal distribution experiment
    2) heavy_hitters - Stores helpers for all the heavy hitter algorithms and the Exponential dist experiment


# ----------------- Running Code -------------------------

To run the default simulations that will generate results similar to the ones you see in the report you need to run method's within the simulation_runner.py file:
    1) You will need to manually run one of the methods in ./simulations/simulation_runner.py
        These methods are commented, and explain how they correspond to a plot in the report
    2) All plots and metrics are generated and saved under ./simulations/frequency_oracles/plots


To view the results of the NYC experiment, these are in a Jupyter notebook
    1) Run your Jupyter notebook server and open ./simulations/frequency_oracles/NYCTaxiSimulation.ipynb
    2) WARNING: All of the Jupyter notebook code will take a while since the dataset is quite large (and various data pre-processing is done i.e clustering)