from copy import deepcopy

from mclt.utils.config import load_config
from mclt.utils.experiments import create_baseline_model_trainer, create_datamodule, run_experiment

config = load_config('train')
config.update(load_config(config['method']))

datamodule = create_datamodule(config)
datamodule.prepare_data()
datamodule.setup()

for repeat in range(config['num_repeats']):
    config = deepcopy(config)
    config['model_random_state'] += repeat

    run_experiment(
        config,
        model_trainer=create_baseline_model_trainer(config, datamodule.num_labels),
        datamodule=datamodule,
        experiment_name=config['dataset'],
        experiment_tag=config['method'],
    )
