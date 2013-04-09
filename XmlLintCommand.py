import sublime
import sublime_plugin
import subprocess


class XmlLintCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        command = "XMLLINT_INDENT=$'    ' xmllint --format --encode utf-8 -"

        p = subprocess.Popen(command, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        result, err = p.communicate(self.view.substr(self.view.sel()[0]).encode('utf-8'))

        if err != "":
            self.view.set_status('xmllint', "xmllint: " + err)
            sublime.set_timeout(self.clear, 10000)

        else:
            self.view.replace(edit, self.view.sel()[0], result.decode('utf-8'))
            sublime.set_timeout(self.clear, 0)
            sublime.status_message("xmllint success")

    def clear(self):
        self.view.erase_status('xmllint')
