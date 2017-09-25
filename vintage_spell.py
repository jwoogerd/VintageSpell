import os
import sys

import sublime
import sublime_plugin

sys.path.append(os.path.join(os.path.dirname(__file__), "pyenchant"))
import enchant

class VintageSpellCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        # dictionary_path = view.settings().get("dictionary")
        # path = sublime.packages_path()
        self.dictionary = enchant.Dict("en_US")


    def run(self, edit, mode):
        region = self.view.sel()[0]
        word = self.view.word(region)
        text = self.view.substr(word)

        if self.dictionary.check(text) == False:
            try:
                suggestions = self.dictionary.suggest(text)
                selection = suggestions[0]
                if mode == 'replace_first':
                    self._replace_with(edit, word, selection)
                elif mode == 'show_list':
                    self._show_list(edit, word, suggestions)
            except IndexError:
                sublime.status_message('No spelling suggestions')


    def _replace_with(self, edit, word, selection):
        self.view.replace(edit, word, selection)


    def _show_list(self, edit, word, suggestions):
        def on_done(index):
            if index > -1:
                self._replace_with(edit, word, suggestions[index])

        self.view.window().show_quick_panel(
            suggestions, on_done, sublime.MONOSPACE_FONT)
