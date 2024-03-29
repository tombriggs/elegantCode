import sys

import chatgptEvaluator
import complexityStatsGen
import evaluateProgram
import processHumanRatings
import eleganceModel

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


if __name__ == '__main__':
    # get the directory name from the command line arguments
    num_args = len(sys.argv)
    if num_args < 4 or (num_args == 3 and sys.argv[1] == '-h'):
        print("Usage:\n\tpython elegantCode.py -c <code-samples-dirname> <output file>")
        print("or")
        print("\tpython elegantCode.py -g <code-samples-dirname> <output file>")
        print("or")
        print("\tpython elegantCode.py -s <complexity rating> <program file> [model]")
        print("or")
        print("\tpython elegantCode.py -h <human-ratings-dirname> <output file root>")
        print("or")
        print("\tpython elegantCode.py -m <human-ratings-dirname> <complexity stats file> [model output file root] [test/train random seed]")
        sys.exit(1)

    run_mode = sys.argv[1]
    if run_mode == '-c':
        complexityStatsGen.calculate_stats_for_dirtree(sys.argv[2], sys.argv[3])
    elif run_mode == '-g':
        chatgptEvaluator.ask_chatgpt_for_dirtree(sys.argv[2], sys.argv[3])
    elif run_mode == '-s':
        model_name = None
        if num_args >= 5:
            model_name = sys.argv[4]
        evaluateProgram.score_program(sys.argv[2], sys.argv[3], model_name)
    elif run_mode == '-h':
        human_ratings_data = processHumanRatings.process_human_ratings_dir(sys.argv[2])
        processHumanRatings.validate_survey_responses(human_ratings_data, sys.argv[3])
        processHumanRatings.write_human_ratings(human_ratings_data)
    elif run_mode == '-m':
        output_file_name = None
        if num_args >= 5:
            output_file_name = sys.argv[4]

        test_train_random_seed = 42
        if num_args >= 6:
            test_train_random_seed = int(sys.argv[5])

        human_ratings = processHumanRatings.process_human_ratings_dir(sys.argv[2])
        eleganceModel.generate_elegance_model(human_ratings, sys.argv[3], output_file_name, test_train_random_seed)

