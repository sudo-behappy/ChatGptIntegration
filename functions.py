import openai
import time
import os


def gpt(chat_list, time_list):
    try:
        openai.api_key = open("env", "r", encoding="utf-8").read()
    except FileNotFoundError:
        with open("env", "w+", encoding="utf-8") as f:
            openai.api_key = input("type in your API key:(shaped like sk-xxxxxxxxxxxxxxxxxxxxxx)")
            f.write(openai.api_key)
    while True:
        str_in = multiline_input(r"let's chat(type anything, or \h for help):").strip("\n")
        match str_in:
            case r"\h":
                print(r"""
\n: new chat
\q: quit and save chat
\h: display this message
                """)
            case r"\q":
                message_time = time.strftime(r"%Y_%m_%d_%H_%M_%S", time.localtime())
                save_chat(chat_list, time_list, message_time)
                exit("chat record saved as: {}.txt".format(message_time))
            case r"\n":
                message_time = time.strftime(r"%Y_%m_%d_%H_%M_%S", time.localtime())
                save_chat(chat_list, time_list, message_time)
                chat_list = []
                time_list = []
                print("new chat started, old chat data saved and then purged")
            case _:
                try:
                    print("wait...don't touch anything...")
                    chat_list.append({"role": "user", "content": str_in})
                    message_time = time.strftime(r"%Y_%m_%d_%H_%M_%S", time.localtime())
                    time_list.append(message_time)
                    try:
                        result = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=chat_list
                        )
                    except Exception:
                        exception_save(chat_list, time_list, "Api fetch failed, chat saved")
                    result["choices"][0]["message"]["content"] = result["choices"][0]["message"]["content"].strip("\n")
                    print(str(result["choices"][0]["message"]["content"]))
                    returning = result["choices"][0]["message"]
                    message_time = time.strftime(r"%Y_%m_%d_%H_%M_%S", time.localtime())
                    time_list.append(message_time)
                    chat_list.append({"content": str(returning["content"]), "role": returning["role"]})
                except Exception:
                    exception_save(chat_list, time_list, "unknown error, chat saved")


def exception_save(chat_list, time_list, message):
    message_time = time.strftime(r"%Y_%m_%d_%H_%M_%S", time.localtime())
    time_list.append(message_time)
    chat_list.append({"content": message, "role": "assistant"})
    save_chat(chat_list, time_list, message_time)
    exit(message + " as {}.txt".format(message_time))


def save_chat(chat_list, time_list, name):
    try:
        os.mkdir("history/")
    except FileExistsError:
        pass
    with open(file=r"history\{}.txt".format(name), mode="w", encoding="utf-8") as f:
        for i in range(len(chat_list)):
            f.write("[{}] {}: {}\n".format(
                time_list[i],
                "GPT" if chat_list[i]["role"] in ["assistant"] else "USER",
                chat_list[i]["content"]
             ))


def multiline_input(message):
    print(message, end="")
    lines = ""
    while True:
        try:
            line = input()
            if line:
                lines += line + "\n"
            else:
                break
        except EOFError:
            break
    return lines


chat_list = []
time_list = []

gpt(chat_list, time_list)
