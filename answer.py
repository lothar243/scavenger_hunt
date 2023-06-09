import os
import sys
import random
import hashlib
import hide_clues as gc
import subprocess

def check_answer(clue, answer):
    if (clue == 1):
        return int(answer) == 42
    elif (clue == 2):
        count = len(os.listdir("/usr"))
        return int(answer) == count
    elif (clue == 3):
        hostname = open("/etc/hostname", "r").read().strip()
        return answer == hostname
    elif (clue == 4):
        return answer in ["i","n","-i","-n"]
    elif (clue == 5):
        return answer == os.getenv("PATH").split(":")[0]
    elif (clue == 6):
        return answer == subprocess.Popen(["which", "python3"], bufsize=0, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip()
    elif (clue == 7):
        if os.geteuid() != 0:
            exit("Please rerun the program with sudo privileges")
        return answer == subprocess.Popen(["ls", "/sys/kernel/debug"], bufsize=0, stdout=subprocess.PIPE).stdout.read().decode("utf-8").split()[0]
    elif (clue == 8):
        return answer == subprocess.Popen(["wc", "-l", "/usr/share/dict/words"], bufsize=0, stdout=subprocess.PIPE).stdout.read().decode("utf-8").split()[0]
    elif (clue == 9):
        return answer == subprocess.Popen(["grep", "-A", "1", "tactful", "/usr/share/dict/words"], bufsize=0, stdout=subprocess.PIPE).stdout.read().decode("utf-8").split('\n')[1]
    elif (clue == 10):
        return answer in ("-k 5 -n -r", "-k 5 -r -n", "-r -k 5 -n", "-r -n -k 5",\
            "-n -r -k 5", "-n -k 5 -r", "-n -r", "-r -n")
    elif (clue == 11):
        if answer == gc.zero_pad(gc.gen_clue_list(gc.START_CLUE, gc.LAST_CLUE, gc.CLUE_SPACE)[11]):
            exit("Congratulations on finding the final clue!")


if __name__ == "__main__":

    if (len(sys.argv) != 3):
        clue_number = int(input("Which clue are you currently working on? "))
        answer = input("and what is your answer for this clue? ")
    else:
        secret_number = int(sys.argv[1])
        clue_number = int(sys.argv[2])
        answer=int(sys.argv[3])

    clue_indexes = gc.gen_clue_list(gc.START_CLUE, gc.LAST_CLUE,
                                    gc.CLUE_SPACE)
    #print clue_indexes
    if (check_answer(clue_number, answer)):
        nextclue_location = gc.zero_pad(clue_indexes[clue_number - gc.START_CLUE + 1])
    else:
        R = random.Random()
        with open(".seed","r") as seedfile:
            seed = int(seedfile.readline())
        if (type(answer) == str):
            md5 = hashlib.md5(answer.encode('utf-8'))
            answer_number = int(md5.hexdigest(),16)
        else:
            answer_number = answer
        R.seed(seed + clue_number + answer_number)
        nextclue_location = gc.zero_pad(R.randint(1, gc.CLUE_SPACE))
    next_clue_number = clue_number + 1
    print("Assuming this is the correct answer, you can find clue {} in clues/{}/clue".format(next_clue_number, nextclue_location))
    print("But remember: Garbage in, garbage out - If you gave me the wrong answer, the clue won't be there.")



