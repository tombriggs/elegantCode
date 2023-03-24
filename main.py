import sys
import subprocess
import lizard
import json
import os
from pygount import SourceAnalysis


# open the file in read mode
#with open(file_path, "r") as file:
    # read the contents of the file
    #file_contents = file.readlines()

    # count the number of non-blank, non-comment lines
    #num_lines_of_code = 0
    #for line in file_contents:
    #    # remove leading/trailing whitespace from the line
    #    stripped_line = line.strip()

        # ignore blank lines and comment-only lines
        #if stripped_line == "" or stripped_line.startswith("#"):
        #    continue

        # increment the count for lines of code
        #num_lines_of_code += 1

    # print the number of lines of code
    #print(f"The file '{file_path}' has {num_lines_of_code} lines of code.")


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def generate_stats(name):
  file_stats = {}

  # Pygount (lines of code)
  pygount = SourceAnalysis.from_file(file_path, "eleganceStats")
  #print(pygount)
  file_stats["nloc_pygount"] = pygount.source_count
  file_stats["comment_count"] = pygount.documentation_count
  file_stats["empty_count"] = pygount.empty_count

  # Lizard (complexity)
  liz = lizard.analyze_file(file_path)
  #print(liz.__dict__)
  file_stats["nloc_lizard"] = liz.nloc
  file_stats["token_count"] = liz.token_count
  file_stats["num_functions"] = len(liz.function_list)
  #for f in liz.function_list:
  #  print("=== " + f.name)
  #  print(f.__dict__)

  func_ccs = [f.cyclomatic_complexity for f in liz.function_list]
  file_stats["min_func_cc"] = min(func_ccs)
  file_stats["max_func_cc"] = max(func_ccs)
  file_stats["avg_func_cc"] = sum(func_ccs)/len(func_ccs)

  token_counts = [f.token_count for f in liz.function_list]
  file_stats["min_token_count"] = min(token_counts)
  file_stats["max_token_count"] = max(token_counts)
  file_stats["avg_token_count"] = sum(token_counts)/len(token_counts)

  # TODO: Do we need to capture top_nesting_level, fan_in, fan_out, general_fan_out?
  # What are they??

  # multimetric
  mm_output = subprocess.run(["multimetric", file_path], capture_output=True, text=True)
  #print(mm_output)
  mm_result = json.loads(mm_output.stdout)
  #print(mm_result)
  # There should be only 1...
  for f in mm_result["overall"]:
    file_stats["mm_" + f] = mm_result["overall"][f]

  return file_stats

if __name__ == '__main__':
    # get the filename from the command line arguments
    if len(sys.argv) < 3:
        print("Usage: python codeStatsGenerator.py <label> <filename>")
        sys.exit(1)
    file_label = sys.argv[1]
    file_path = sys.argv[2]
    file_stats = generate_stats(file_path)

    file_stats_header = "filesource,filename,"
    file_stats_header += ','.join(str(x) for x in file_stats.keys())
    print(file_stats_header)

    file_stats_str = "\"" + file_label + "\",\"" + os.path.basename(file_path) + "\","
    file_stats_str += ','.join(str(x) for x in file_stats.values())
    print(file_stats_str)

