import os
import subprocess
import lizard
import json
from pygount import SourceAnalysis


def generate_stats(file_path, problem_num, file_label, print_header):
    file_stats = calculate_stats(file_path)

    if print_header:
        file_stats_header = "filesource,problem_num,filename,"
        file_stats_header += ','.join(str(x) for x in file_stats.keys())
        print(file_stats_header)

    file_stats_str = '"' + file_label + '","' + problem_num + '","' + os.path.basename(file_path) + '",'
    file_stats_str += ','.join(str(x) if x is not None else "" for x in file_stats.values())
    print(file_stats_str)


def calculate_stats(file_path):
    file_stats = {}

    # Pygount (lines of code)
    pygount = SourceAnalysis.from_file(file_path, "eleganceStats")
    # print(pygount)
    file_stats["nloc_pygount"] = pygount.source_count
    file_stats["comment_count"] = pygount.documentation_count
    file_stats["empty_count"] = pygount.empty_count

    # Lizard (complexity)
    liz = lizard.analyze_file(file_path)
    # print(liz.__dict__)
    file_stats["nloc_lizard"] = liz.nloc
    file_stats["token_count"] = liz.token_count
    file_stats["num_functions"] = len(liz.function_list)
    # for f in liz.function_list:
    #  print("=== " + f.name)
    #  print(f.__dict__)

    func_ccs = [f.cyclomatic_complexity for f in liz.function_list]
    if func_ccs:
        file_stats["min_func_cc"] = min(func_ccs)
        file_stats["max_func_cc"] = max(func_ccs)
        file_stats["avg_func_cc"] = sum(func_ccs) / len(func_ccs)
    else:
        file_stats["min_func_cc"] = None
        file_stats["max_func_cc"] = None
        file_stats["avg_func_cc"] = None

    token_counts = [f.token_count for f in liz.function_list]
    if token_counts:
        file_stats["min_token_count"] = min(token_counts)
        file_stats["max_token_count"] = max(token_counts)
        file_stats["avg_token_count"] = sum(token_counts) / len(token_counts)
    else:
        file_stats["min_token_count"] = None
        file_stats["max_token_count"] = None
        file_stats["avg_token_count"] = None

    # TODO: Do we need to capture top_nesting_level, fan_in, fan_out, general_fan_out?
    # What are they??

    # multimetric
    mm_output = subprocess.run(["multimetric", file_path], capture_output=True, text=True)
    # print(mm_output)
    mm_result = json.loads(mm_output.stdout)
    # print(mm_result)
    # There should be only 1...
    for f in mm_result["overall"]:
        file_stats["mm_" + f] = mm_result["overall"][f]

    return file_stats


if __name__ == '__main__':
  # get the filename from the command line arguments
  num_args = len(sys.argv)
  if num_args < 3:
    print("Usage: python complexityStatsGen.py <label> <filename>")
    sys.exit(1)
  file_label = sys.argv[1]
  file_path = sys.argv[2]

  print_header = (num_args >= 4 and sys.argv[3] == "--header")
