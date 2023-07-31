import pandas as pd
import re
import os

# uploaded = files.upload()

def fix_column_name(n):
    n = n.replace("How many years of experience do you have programming in... >> ", "exp_w_")
    n = n.replace("Total Years of Programming Experience", "exp_total")
    n = re.sub('Evaluation - Solution (\d) +>> ', "S\\1_", n)
    n = n.replace('Overall Elegance', 'Overall')
    return n


def process_human_ratings_file(file_name, problem_num, solution_list, evaluator_features):
    features = pd.read_csv(file_name, na_filter=False)

    features.rename(columns=lambda n: fix_column_name(n), inplace=True)

    if evaluator_features is None:
        evaluator_features = features.iloc[:, 0:10]

        columns_to_replace = ['exp_w_Java', 'exp_w_Python', 'exp_w_C', 'exp_w_C++', 'exp_total']
        for column_name in columns_to_replace:
            evaluator_features[column_name].replace({'None': 0, '< 1': 1, '1 - 2': 2, '3 - 5': 3, '5 - 10': 4, '10+': 5}, inplace=True)

    submission_info = features.loc[:, 'Submission Date':'Submission IP']
    solution_info = []

    for solnum in range(1, 6):
        sol_features_only = features.loc[:, "S%d_Readability" % solnum:"S%d_Overall" % solnum].copy()
        sol_features_only.rename(columns=lambda n: n.replace("S%d_" % solnum, ""), inplace=True)
        sol_features_only.replace({'Not at All': 1, 'A little': 2, 'Somewhat': 3, 'Mostly': 4, 'Very much': 5}, inplace=True)

        #sol_features_only = pd.get_dummies(sol_features_only)

        #if has_evaluator_info:
        #    # Put everything back together
        #    sol_features = pd.concat([evaluator_features.reset_index(drop=True),
        #                              sol_features_only.reset_index(drop=True)],
        #                         axis=1)
        #else:
        sol_features_plus_subinfo = pd.concat([submission_info, sol_features_only], axis=1)
        # Match evaluator info to evaluations by date and IP
        sol_features = pd.merge(sol_features_plus_subinfo, evaluator_features, how='inner',
                                    left_on=['Submission Date', 'Submission IP'],
                                    right_on=['Submission Date', 'Submission IP'])

        # Can't do anything without an overall rating...
        sol_features = sol_features[sol_features['Overall'] != '']

        sol_info = dict(solution_list[solnum - 1])
        sol_info['problem_number'] = problem_num
        sol_info['features'] = sol_features
        sol_info['average_overall'] = sol_features['Overall'].mean()
        sol_info['weighted_overall'] = (sol_features['Overall'] * (0.7 + (sol_features['exp_total']/10))).mean()
        #print("Average: {} Weighted: {}".format(sol_info['average_overall'], sol_info['weighted_overall']))

        solution_info.append(sol_info)

    return solution_info, evaluator_features


def process_human_ratings_dir(dirname):
    manifest_file = 'MANIFEST.csv'

    file_list = os.listdir(dirname)
    print(file_list)

    human_ratings_data = None

    if manifest_file in file_list:
        ratings_files = pd.read_csv(dirname + os.sep + manifest_file)

        human_ratings_data = []

        # Assume that the first file has the evaluator info in it -
        # the first call will fill this in, subsequent calls will send it back
        evaluator_features = None

        for index, ratings_file_info in ratings_files.iterrows():
            ratings_file_name = ratings_file_info['filename']
            ratings_file_problem_num = ratings_file_info['problem_num']
            if ratings_file_name in file_list:
                solution_list = []
                for solution_num in range(1, 6):
                    this_author = ratings_file_info['author' + str(solution_num)]
                    this_filename = ratings_file_info['source_file' + str(solution_num)]
                    solution_list.append({'author': this_author, 'source_file': this_filename})

                one_ratings_file, evaluator_features = \
                    process_human_ratings_file(dirname + os.sep + ratings_file_name,
                                               ratings_file_problem_num, solution_list, evaluator_features)

                human_ratings_data.append(one_ratings_file)

    #print(human_ratings_data)
    return human_ratings_data

