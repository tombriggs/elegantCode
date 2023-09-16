import os
import sys

import openai

openai.api_key = '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'

# NOTE: This won't work correctly unless nayuki's solutions to problem 54
# (poker hands) are shortened. The _short versions of the solutions
# in that directory represent fixes for that. To get this to run
# it will also be necessary to modify the MANIFEST file to point to the
# _short versions.

def generate_chatgpt_stats(file_path, problem_num, file_label, print_header, outfile):
    print("Asking ChatGPT about problem " + problem_num + " file_label " + file_label)
    file_stats = ask_chatgpt(file_path)

    if print_header:
        file_stats_header = "filesource,problem_num,filename,"
        file_stats_header += ','.join(str(x) for x in file_stats.keys())
        print(file_stats_header, file=outfile)

    file_stats_str = '"' + file_label + '","' + problem_num + '","' + os.path.basename(file_path) + '",'
    file_stats_str += ','.join(str(x) if x is not None else "" for x in file_stats.values())
    print(file_stats_str, file=outfile)


def ask_chatgpt(file_path):
    gpt_model_name = "gpt-3.5-turbo"
    #gpt_model_name = "gpt-4-32k"

    file_stats = {}

    with open(file_path, "r") as file:
        # read the contents of the file
        file_contents = file.read()

    messages = [{"role": "system", "content": "You are an intelligent assistant."}]
    message = "Please tell me in 20 words or less, on a scale of 1 to 5, how elegant is this program?\n" + file_contents
    messages.append({"role": "user", "content": message})

    chat = openai.ChatCompletion.create(model=gpt_model_name, messages=messages)
    reply = chat.choices[0].message.content
    file_stats['reply'] = reply
    #print(f"ChatGPT: {reply}")
    #messages.append({"role": "assistant", "content": reply})

    return file_stats


def ask_chatgpt_for_dirtree(file_path, outfile_name):
    samples_dict = {}

    outfile = sys.stdout
    if outfile_name != 'stdout':
        outfile = open(outfile_name, "w")

    for root, dirs, files in os.walk(file_path):
        for name in files:
            if name == 'MANIFEST':
                # print(os.path.join(root, name))
                with open(os.path.join(root, name), "r") as file:
                    # read the contents of the file
                    file_contents = [s for s in file.read().splitlines() if s]
                    # print(file_contents)
                    solution_list = [line.split(' ') for line in file_contents[1:]]
                    samples_dict[file_contents[0]] = solution_list
        # for name in dirs:
        #    print(os.path.join(root, name))

    # print(samples_dict)
    solution_num = 1
    for dirname in samples_dict.keys():
        for solution in samples_dict[dirname]:
            problem_num = solution[0]
            filename = solution[1]
            full_filename = file_path + os.sep + dirname + os.sep + filename

            generate_chatgpt_stats(full_filename, problem_num, dirname, (solution_num == 1), outfile)
            solution_num += 1

    if outfile_name != 'stdout':
        outfile.close()

