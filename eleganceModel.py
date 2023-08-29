import pandas as pd
import numpy as np
from statistics import mean
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

#problem_complexities = {1: 1, 2: 1, 54: 2, 74: 3}
problem_complexities = {1: 5, 2: 5, 54: 10, 74: 15}


def generate_elegance_model(human_ratings, complexity_stats_file):
    complexity_stats_raw = pd.read_csv(complexity_stats_file)

    # Generate a unique key for each file by combining the author/source and file name
    complexity_stats_raw["item_key"] = complexity_stats_raw["filesource"] + ":" + complexity_stats_raw["filename"]

    average_fields = ['average_overall', 'total_weighted_overall',
                      'lang_weighted_overall', 'total_and_lang_weighted_overall']
    #average_field_name = 'average_overall'
    #average_field_name = 'total_weighted_overall'
    #average_field_name = 'lang_weighted_overall'
    #average_field_name = 'total_and_lang_weighted_overall'

    average_ratings_dict = {}
    # structure of human_ratings is [problem_num][solution_num]
    for oneProblemRatings in human_ratings:
        for oneSolutionRatings in oneProblemRatings:
            # avgOverall = oneSolutionRatings['features']['Overall'].mean()
            dict_key = oneSolutionRatings['author'] + ':' + oneSolutionRatings['source_file']

            average_ratings_dict_sol = {}
            for average_field_name in average_fields:
                average_ratings_dict_sol[average_field_name] = oneSolutionRatings['average_scores'][average_field_name]

            average_ratings_dict[dict_key] = average_ratings_dict_sol

    complexity_stats_raw['averageOverall'] = complexity_stats_raw['item_key'].map(average_ratings_dict)
    complexity_stats_raw['problemComplexity'] = complexity_stats_raw['problem_num'].map(problem_complexities)

    complexity_stats_raw['avg_func_cc_to_complexity_ratio'] = complexity_stats_raw['avg_func_cc'] / complexity_stats_raw['problemComplexity']
    complexity_stats_raw['max_func_cc_to_complexity_ratio'] = complexity_stats_raw['max_func_cc'] / complexity_stats_raw['problemComplexity']

    complexity_stats = complexity_stats_raw[complexity_stats_raw['averageOverall'].notna()]

    #####
    # copy-paste-modify from https://towardsdatascience.com/random-forest-in-python-24d0893d51c0
    #####

    # Labels are the values we want to predict
    # labels = np.array(features['actual'])
    labels = np.array(complexity_stats['averageOverall'])

    # Remove the labels, internal bookkeeping values,
    # and we've determined aren't important from the features
    # axis 1 refers to the columns
    # features = features.drop('actual', axis=1)
    columns_to_drop = ['averageOverall', 'filesource', 'filename', 'item_key', 'problem_num',
                       'mm_fanout_internal', 'mm_loc', 'mm_maintainability_index', 'mm_pylint',
                       'mm_tiobe_compiler', 'mm_tiobe_coverage', 'mm_tiobe_duplication', 'mm_tiobe_functional',
                       'mm_tiobe_security', 'mm_tiobe_standard'
                       ]
    complexity_stats = complexity_stats.drop(columns_to_drop, axis=1)

    # Saving feature names for later use
    # feature_list = list(features.columns)
    complexity_stats_list = list(complexity_stats.columns)

    # Convert to numpy array
    # features = np.array(features)
    features = np.array(complexity_stats)

    # Split the data into training and testing sets
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.20,
                                                                                random_state=42)

    # Note to self: I think the baseline is simply 3 - i.e. the middle of the range of 1-5
    baseline_preds = np.full((1, len(test_labels)), 3)[0]

    # Instantiate model with 1000 decision trees
    rf = RandomForestRegressor(n_estimators=1000, random_state=42)

    results_dict = {}

    for average_field_name in average_fields:
        # Need the values for just this one field in an array
        train_labels_this_field = [tl[average_field_name] for tl in train_labels]
        test_labels_this_field = [tl[average_field_name] for tl in test_labels]

        results_dict[average_field_name] = {}

        # Train the model on training data
        rf.fit(train_features, train_labels_this_field)

        # Use the forest's predict method on the test data
        predictions = rf.predict(test_features)

        # Calculate the absolute errors
        errors = abs(predictions - test_labels_this_field)
        error_average = mean(errors).round(3)
        results_dict[average_field_name]['errors'] = errors
        results_dict[average_field_name]['error_average'] = error_average
        #print("{} Error: {}, average {}".format(average_field_name, errors, error_average))

        baseline_errors = abs(baseline_preds - test_labels_this_field)
        baseline_error_average = mean(baseline_errors).round(3)
        results_dict[average_field_name]['baseline_errors'] = baseline_errors
        results_dict[average_field_name]['baseline_error_average'] = baseline_error_average
        #print("{} Baseline errors: {}, average {}".format(average_field_name, baseline_errors, baseline_error_average))

        improvements = baseline_errors - errors
        improvement_average = mean(improvements).round(3)
        results_dict[average_field_name]['improvements'] = improvements
        results_dict[average_field_name]['improvements_average'] = improvement_average
        #print("{} Improvement: {}, average {}".format(average_field_name, improvements, improvement_average))

    print("Improvements")
    print("------------")
    for average_field_name in average_fields:
        print("{}: {}".format(average_field_name, results_dict[average_field_name]['improvements_average']))

    """
    # Get numerical feature importances
    importances = list(rf.feature_importances_)

    # List of tuples with variable and importance
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(complexity_stats_list, importances)]

    # Sort the feature importances by most important first
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

    # Print out the feature and importances
    print("\nVariable Importance")
    print("-----------------------")
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];
    """

    """
    # Create a new random forest with only the most important variables
    rf_most_important = RandomForestRegressor(n_estimators=1000, random_state=42)

    # Extract the most important features
    important_indices = [complexity_stats_list.index('avg_token_count'), complexity_stats_list.index('max_token_count'),
                         complexity_stats_list.index('min_token_count'), complexity_stats_list.index('mm_fanout_external'),
                         complexity_stats_list.index('problemComplexity'), complexity_stats_list.index('empty_count'),
                         complexity_stats_list.index('mm_comment_ratio'), complexity_stats_list.index('nloc_pygount'),
                         complexity_stats_list.index('comment_count'), complexity_stats_list.index('mm_halstead_difficulty'),
                         complexity_stats_list.index('mm_operands_sum'), complexity_stats_list.index('mm_operators_uniq')]
    train_important = train_features[:, important_indices]
    test_important = test_features[:, important_indices]

    average_field_name = 'total_weighted_overall'

    # Train the second random forest
    train_labels_weighted_total = [tl[average_field_name] for tl in train_labels]
    rf_most_important.fit(train_important, train_labels_weighted_total)

    # Make predictions and determine the error
    test_labels_weighted_total = [tl[average_field_name] for tl in test_labels]
    predictions = rf_most_important.predict(test_important)
    errors = abs(predictions - test_labels_weighted_total)
    error_average = mean(errors).round(3)

    baseline_errors = abs(baseline_preds - test_labels_weighted_total)
    baseline_error_average = mean(baseline_errors).round(3)

    improvements = baseline_errors - errors
    improvements_average = mean(improvements).round(3)
    print("Improvement")
    print("------------")
    print("{}: {}".format(average_field_name, improvements_average))
    """
