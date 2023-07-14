import sys
import complexityStatsGen
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
    if num_args < 4:
        print("Usage:\n\tpython elegantCode.py -c <code-samples-dirname> <output file>")
        print("or")
        print("\tpython elegantCode.py -h <human-ratings-dirname>")
        print("or")
        print("\tpython elegantCode.py -m <human-ratings-dirname> <complexity stats file>")
        sys.exit(1)

    if sys.argv[1] == '-c':
        complexityStatsGen.calculate_stats_for_dirtree(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == '-h':
        processHumanRatings.process_human_ratings_dir(sys.argv[2])
    elif sys.argv[1] == '-m':
        human_ratings = processHumanRatings.process_human_ratings_dir(sys.argv[2])
        eleganceModel.generate_elegance_model(human_ratings, sys.argv[3])

