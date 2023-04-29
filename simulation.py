"""
Source:
https://github.com/iosband/ts_tutorial
Plots are saved to /plot/ by default
"""


import importlib
import os
import plotnine as gg
import base.plot as bp
import sys

from base import config_lib


def simulate(config='graph.config_correlated', job_id = 0, save_path = 'tmp'):
    print('Running the simulation...')

    experiment_config = importlib.import_module(config)
    config = experiment_config.get_config()

    # Running the experiment.
    job_config = config_lib.get_job_config(config, job_id)
    experiment = job_config['experiment']
    experiment.run_experiment()

    # Saving results to csv.
    file_name = ('exp=' + config.name + '-id=' + str(job_id) + '.csv')
    file_path = os.path.join(save_path, file_name)
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    with open(file_path, 'w') as f:
        experiment.results.to_csv(f, index=False)

    # Save the parameters if it is the first job.
    if job_id == 0:
        params_df = config_lib.get_params_df(config)
        file_name = 'exp=' + config.name + '-params.csv'
        file_path = os.path.join(save_path, file_name)
        with open(file_path, 'w') as f:
            params_df.to_csv(f, index=False)


simulate(job_id=0)
simulate(job_id=1)
##############################################################################
print('Plotting...')

sys.path.append(os.getcwd())
gg.theme_set(gg.theme_bw(base_size=16, base_family='serif'))

_DATA_FILEPATH = 'tmp'  # .csv files of experiments
_PLOT_FILEPATH = 'plot'  # where you want to save plots
if not os.path.isdir(_PLOT_FILEPATH):
    os.makedirs(_PLOT_FILEPATH)

bp.set_data_path(_DATA_FILEPATH)

plot_dict = {}

# Most plots are simple instantaneous regret
plot_dict.update(bp.simple_algorithm_plot('graph_correlated'))

# Graph plots also do cumulative distance
plot_dict.update(bp.cumulative_travel_time_plot('graph_correlated'))

# Ensemble plots
plot_dict.update(bp.ensemble_plot('graph_correlated'))

# Saving all plots to file

for plot_name, p in plot_dict.items():
    file_path = os.path.join(_PLOT_FILEPATH, plot_name.lower() + '.png')
    file_path = file_path.replace(' ', '_')
    if 'ensemble' in file_path:
        p.save(file_path, height=8, width=6)
    else:
        p.save(file_path, height=8, width=8)

