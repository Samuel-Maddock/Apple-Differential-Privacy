# ---------- Installation -------------

To install dependencies for the project when in the root directory run:
    python -m pip install -r ./requirements.txt

# --------------- Structure of Code ------------------

All the code for the algorithms are under the algorithms module:
    1) apple_ldp - Implementations of CMS, HCMS and SFP
    2) bnst_ldp - Implementations of TreeHistogram, Private Count Sketch, Hashtogram, SuccinctHist, ExplicitHist, Bitstogram
    3) RAPPOR -  Python 3 implementation and wrapper of Google's RAPPOR (client + server side)

All of the simulation framework code is within the simulation module:
    1) frequency_oracles - Stores wrappers and helpers for all the frequency oracle algorithms, and store code for the Normal distribution experiment
    2) heavy_hitters - Stores helpers for all the heavy hitter algorithms and the Exponential dist experiment

# ----------------- Running Code -------------------------

To run the default simulations that will generate results similar to the ones you see in the report you need to run methods within the simulation_runner.py file:
    1) You will need to manually run one of the methods in ./simulations/simulation_runner.py
        These methods are commented, and explain how they correspond to a plot in the report
    2) All plots and metrics are generated and saved under ./simulations/frequency_oracles/plots

For NYC Taxicab heatmaps:
    1) All of the heatmaps generated have been saved as .html files under ./simulations/frequency_oracles/Heatmaps
    2) All you need to do to view them is open them in a browser

For running the actual simulation code for the NYC analysis this is done in a Jupyter Notebook
    1) Run your Jupyter notebook server and open ./simulations/frequency_oracles/NYCTaxiSimulation.ipynb
    2) WARNING: All of the Jupyter notebook code will take a while since the dataset is quite large (and various data pre-processing is done i.e clustering)