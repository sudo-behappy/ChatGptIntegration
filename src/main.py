import sys
import traceback
from PyQt5 import QtWidgets
from main_ui import Ui_ChatGPTIntergration
import functions
import platform
import pyperclip
import time
import os
import re


class Application(QtWidgets.QMainWindow, Ui_ChatGPTIntergration):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        super(Ui_ChatGPTIntergration, self).__init__()
        self.setupUi(self)
        self.chat_list = []
        self.time_list = []
        self.CommandRecord.appendPlainText("-" * 20 + "WELCOME" + "-" * 20)
        content = ''
        try:
            with open("env", "r", encoding="utf-8") as f:
                content = f.read()
            self.update_api_key(content)
        except FileNotFoundError:
            open("env", "w+", encoding="utf-8")

    def update_command_string(self, string):
        self.CommandRecord.appendPlainText(string)

    def continue_chat(self):
        self.update_command_string("功能还未实装，暂时无法使用")
        # self.chat_purge_and_save()
        # self.resume_chat(self.ChatPath.text())

    def upload_chat_content(self):
        """
        upload the chat content to chatgpt and yield reply
        :return:
        """
        chat_content = self.ChatContent.toPlainText()
        self.ChatContent.clear()
        self.time_list.append(functions.get_time())
        self.chat_list.append({"role": "user", "content": chat_content})
        try:
            start = time.time()
            result = functions.openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.chat_list
            )
            result["choices"][0]["message"]["content"] = result["choices"][0]["message"]["content"].strip("\n")
            returning = result["choices"][0]["message"]
            self.time_list.append(functions.get_time())
            self.chat_list.append({"content": str(returning["content"]), "role": returning["role"]})
            result = str(result["choices"][0]["message"]["content"])
            self.ChatRecord.appendPlainText("-" * 20 + "\n" + result)
        except Exception as e:
            result = traceback.format_exc()
            self.update_command_string(result)
            self.update_command_string("请将这个信息截图并发送给开发者")
        end = time.time()
        self.update_command_string("result obtained in {} seconds".format(str(end - start)))

    def chat_purge_without_save(self):
        """
        purge the chat data without saving it and start a new chat
        :return:
        """
        self.ChatRecord.clear()
        self.chat_list = []
        self.time_list = []

    def chat_purge_and_save(self):
        """
        save and purge the chat data then start a new chat
        :return:
        """
        self.ChatRecord.clear()
        functions.save_chat(self.chat_list, self.time_list, functions.get_time())
        self.chat_purge_without_save()
        self.open_chat_record_folder()

    def open_chat_record_folder(self):
        try:
            os.mkdir("history")
        except FileExistsError:
            pass
        match platform.system():
            case "Windows":
                os.startfile("history")
            case "Darwin":
                # TODO: launch finder via command
                pass
            case "Linux":
                # TODO: launch finder via command
                pass
                os.startfile()
        self.update_command_string("folder opened")

    def show_how_to_apikey(self):
        """
        display this fantastic help
        :return:
        """
        self.VariableHint.clear()
        self.VariableHint.appendPlainText("请管软件开发者要API Key")

    def chat_content_updated(self):
        """
        This method is prepared for future use, now it has no use
        """
        pass

    def update_api_key(self, key_content):
        """
           called when the api_key field is updated.
           :param str key_content: The input value of api_key field
        """
        functions.openai.api_key = key_content
        self.APIkey.setText(key_content)
        with open("env", "w+", encoding="utf-8") as f:
            f.write(key_content)
        self.update_command_string("API key updated")

    def localization_updated(self, locale_index):
        """
        called when localization setting is updated
        :param locale_index: index of selected locale item
        """
        self.VariableHint.setText(str(locale_index))

    def copy_content(self):
        """
        copy the last response from chatgpt
        :return:
        """
        try:
            pyperclip.copy(self.chat_list[len(self.chat_list) - 1]["content"])
            self.update_command_string("last response copied")
        except Exception:
            self.update_command_string("Response list is empty!")

    def paste_content(self):
        """
        paste the content on clipboard to input field
        :return:
        """
        self.ChatContent.setPlainText(pyperclip.paste())
        self.update_command_string("clipboard pasted")

    def clear_log(self):
        """
        clear the command log
        :return:
        """
        self.CommandRecord.clear()

    def lock_api_field(self, is_locked):
        self.APIkey.setEnabled(not is_locked)

    def resume_chat(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                user = True
                for line in f.read().split("\n"):
                    date = str(re.match(r"\[\d+_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}\]", line))
                    content = str(re.match("(?:USER|GPT):(.*)", line).group(1))
                    print(date, content)
                    self.chat_list.append({"content": content, "role": "user" if user else "assistant"})
                    self.time_list.append(date)
                    user = not user
        except FileNotFoundError:
            self.update_command_string("ERROR: 非法路径")
        self.update_command_string("chat continued...")
                
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    chat_application = Application()
    chat_application.show()
    sys.exit(app.exec_())
