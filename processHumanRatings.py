import pandas as pd
import re
import os

# uploaded = files.upload()

def fix_column_name(n):
    n = n.replace("How many years of experience do you have programming in... >>", "exp_w_")
    n = n.replace("Total Years of Programming Experience", "exp_total")
    n = re.sub('Evaluation - Solution (\d) +>> ', "S\\1_", n)
    n = n.replace('Overall Elegance', 'Overall')
    return n


def process_human_ratings_file(file_name, problem_num, solution_list):
    features = pd.read_csv(file_name)

    features.rename(columns=lambda n: fix_column_name(n), inplace=True)

    evaluator_features = features.iloc[:, 1:8]

    solution_info = []
    for solnum in range(1, 6):
        sol_features_only = features.loc[:, "S%d_Readability" % solnum:"S%d_Overall" % solnum].copy()
        sol_features_only.rename(columns=lambda n: n.replace("S%d_" % solnum, ""), inplace=True)
        sol_features_only = pd.get_dummies(sol_features_only)

        # Q: Do we want dummies for the "overall" feature, which is actually our label?

        sol_features = pd.concat([evaluator_features.reset_index(drop=True), sol_features_only.reset_index(drop=True)],
                                 axis=1)

        sol_info = dict(solution_list[solnum - 1])
        sol_info['problem_number'] = problem_num
        sol_info['features'] = sol_features

        solution_info.append(sol_info)

    return solution_info


def process_human_ratings_dir(dirname):
    manifest_file = 'MANIFEST.csv'

    file_list = os.listdir(dirname)
    print(file_list)

    human_ratings_data = None

    if manifest_file in file_list:
        ratings_files = pd.read_csv(dirname + os.sep + manifest_file)

        human_ratings_data = []

        for index, ratings_file_info in ratings_files.iterrows():
            ratings_file_name = ratings_file_info['filename']
            ratings_file_problem_num = ratings_file_info['problem_num']
            if ratings_file_name in file_list:
                solution_list = []
                for solution_num in range(1, 6):
                    this_author = ratings_file_info['author' + str(solution_num)]
                    this_filename = ratings_file_info['source_file' + str(solution_num)]
                    solution_list.append({'author': this_author, 'source_file': this_filename})

                one_ratings_file = process_human_ratings_file(dirname + os.sep + ratings_file_name, ratings_file_problem_num, solution_list)

                human_ratings_data.append(one_ratings_file)

    #print(human_ratings_data)
    return human_ratings_data

