import sys
from copy import deepcopy

from mclt.data import TASK_LANG_MATRIX
from mclt.utils.config import load_config
from mclt.utils.experiments import (
    create_datamodule, run_experiment,
    create_multilingual_model_trainer,
)

config = load_config('train')
config.update(load_config(config['method']))

for task_name, datasets in TASK_LANG_MATRIX.iteritems():
    for lang_name, dataset in datasets.iteritems():
        if dataset is None:
            continue

        config['tasks'] = [task_name]
        config['languages'] = [lang_name]
        for repeat in range(config['num_repeats']):
            config = deepcopy(config)
            config['model_random_state'] += repeat

            run_experiment(
                config,
                create_datamodule=create_datamodule,
                create_model_trainer=create_multilingual_model_trainer,
                experiment_name='baseline',
                experiment_tag=config['method'],
            )
