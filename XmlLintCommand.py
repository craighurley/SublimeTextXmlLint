import sublime
import sublime_plugin
import subprocess


class XmlLintCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        command = "XMLLINT_INDENT=$'    ' xmllint --format --encode utf-8 -"

        # select all text before begining
        self.view.sel().add(sublime.Region(0, self.view.size()))

        # try running xmllint on the select text
        p = subprocess.Popen(command, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        result, err = p.communicate(self.view.substr(self.view.sel()[0]).encode('utf-8'))

        if err != b'':
            # there was an error, report it
            sublime.status_message("xmllint: " + err)
            sublime.set_timeout(self.clear, 10000)

        else:
            # xmllint ran successfully, so replace the selected text
            self.view.replace(edit, self.view.sel()[0], result.decode('utf-8'))
            sublime.set_timeout(self.clear, 0)
            # report success
            sublime.status_message("xmllint: success")
            # clear the selection and place the cursor at the start of the document
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(0, 0))

    def clear(self):
        self.view.erase_status('xmllint')
