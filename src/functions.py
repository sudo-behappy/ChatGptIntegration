import traceback
import openai
import time
import os

def save_chat(chat_list, time_list, name):
    try:
        os.mkdir("./history/")
    except FileExistsError:
        pass
    try:
        with open(r"history\{}.txt".format(name), "w+", encoding="utf-8") as f:
            for i in range(len(chat_list)):
                f.write("[{}] {}: {}\n".format(
                    time_list[i],
                    "GPT" if chat_list[i]["role"] in ["assistant"] else "USER",
                    chat_list[i]["content"]
                 ))
    except Exception:
        print(traceback.format_exc())


def get_time():
    return time.strftime(r"%Y_%m_%d_%H_%M_%S", time.localtime())


