import sys
import os
import complexityStatsGen

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
    if num_args < 2:
        print("Usage: python complexityStatsGenAll.py <dirname>")
        sys.exit(1)
    file_path = sys.argv[1]

    samples_dict = {}

    for root, dirs, files in os.walk(file_path):
        for name in files:
            if name == 'MANIFEST':
                #print(os.path.join(root, name))
                with open(os.path.join(root, name), "r") as file:
                    # read the contents of the file
                    file_contents = [s for s in file.read().splitlines() if s]
                    #print(file_contents)
                    solution_list = [line.split(' ') for line in file_contents[1:]]
                    samples_dict[file_contents[0]] = solution_list
        #for name in dirs:
        #    print(os.path.join(root, name))

    #print(samples_dict)
    solution_num = 1;
    for dirname in samples_dict.keys():
        for solution in samples_dict[dirname]:
            problem_num = solution[0]
            filename = solution[1]
            full_filename = file_path + os.sep + dirname + os.sep + filename

            complexityStatsGen.generate_stats(full_filename, problem_num, dirname, (solution_num == 1))
            solution_num += 1

