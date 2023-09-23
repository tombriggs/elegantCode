import pandas as pd
import numpy as np
from joblib import load

import complexityStatsGen
import eleganceModel


def score_program(complexity_rating, program_file, model_name):
    if model_name is None:
        model_name = 'total_weighted_overall'

    model_file_name = 'eleganceModel_' + model_name + '.joblib'

    rf = load(model_file_name)

    complexity_stats_dict = complexityStatsGen.calculate_stats(program_file)
    complexity_stats = pd.DataFrame([complexity_stats_dict])

    complexity_stats['problemComplexity'] = int(complexity_rating)

    complexity_stats['avg_func_cc_to_complexity_ratio'] = complexity_stats['avg_func_cc'] / complexity_stats['problemComplexity']
    complexity_stats['max_func_cc_to_complexity_ratio'] = complexity_stats['max_func_cc'] / complexity_stats['problemComplexity']

    complexity_stats = eleganceModel.drop_unnecessary_columns(complexity_stats)
    features = np.array(complexity_stats)

    predictions = rf.predict(features)

    print(predictions)
