import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

#problem_complexities = {1: 1, 2: 1, 54: 2, 74: 3}
problem_complexities = {1: 5, 2: 5, 54: 10, 74: 15}


def generate_elegance_model(human_ratings, complexity_stats_file):
    complexity_stats_raw = pd.read_csv(complexity_stats_file)

    # Generate a unique key for each file by combining the author/source and file name
    complexity_stats_raw["item_key"] = complexity_stats_raw["filesource"] + ":" + complexity_stats_raw["filename"]

    average_ratings_dict = {}
    # structure of human_ratings is [problem_num][solution_num]
    for oneProblemRatings in human_ratings:
        for oneSolutionRatings in oneProblemRatings:
            # TODO: I think this value is already available in oneSolutionRatings['average_overall']
            avgOverall = oneSolutionRatings['features']['Overall'].mean()
            average_ratings_dict[oneSolutionRatings['author'] + ':' + oneSolutionRatings['source_file']] = avgOverall

    complexity_stats_raw['averageOverall'] = complexity_stats_raw['item_key'].map(average_ratings_dict)
    complexity_stats_raw['problemComplexity'] = complexity_stats_raw['problem_num'].map(problem_complexities)
    complexity_stats = complexity_stats_raw[complexity_stats_raw['averageOverall'].notna()]

    #####
    # copy-paste-modify from https://towardsdatascience.com/random-forest-in-python-24d0893d51c0
    #####

    # Labels are the values we want to predict
    # labels = np.array(features['actual'])
    labels = np.array(complexity_stats['averageOverall'])

    # Remove the labels (and internal bookkeeping string values) from the features
    # axis 1 refers to the columns
    # features = features.drop('actual', axis=1)
    complexity_stats = complexity_stats.drop(['averageOverall', 'filesource', 'filename', 'item_key'], axis=1)

    # Saving feature names for later use
    # feature_list = list(features.columns)
    complexity_stats_list = list(complexity_stats.columns)

    # Convert to numpy array
    # features = np.array(features)
    features = np.array(complexity_stats)

    # Split the data into training and testing sets
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.20,
                                                                                random_state=42)

    print('Training Features Shape:', train_features.shape)
    print('Training Labels Shape:', train_labels.shape)
    print('Testing Features Shape:', test_features.shape)
    print('Testing Labels Shape:', test_labels.shape)

    # Note to self: I think the baseline is simpy 3 - i.e. the middle of the range of 1-5

    # Instantiate model with 1000 decision trees
    rf = RandomForestRegressor(n_estimators=1000, random_state=42)

    # Train the model on training data
    rf.fit(train_features, train_labels)

    # Use the forest's predict method on the test data
    predictions = rf.predict(test_features)

    # Calculate the absolute errors
    errors = abs(predictions - test_labels)

