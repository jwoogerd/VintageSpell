import sublime_plugin, sublime
import hunspell 

class VintageSpellCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self.dictionary = hunspell.HunSpell('./en_US.dic', './en_US.aff')

    def run(self, edit, mode):
        region = self.view.sel()[0]
        word = self.view.word(region)
        text = self.view.substr(word)

        def replace(selection):
            self.view.replace(edit, word, selection)

        def show_list(text, suggestions):
            def on_done(index):
                if index == -1:
                    return
                else:
                    replace(suggestions[index])

            self.view.window().show_quick_panel(
                suggestions, on_done, sublime.MONOSPACE_FONT)

        if self.dictionary.spell(text) == True:
            return
        else:
            try:
                suggestions = self.dictionary.suggest(text)
                if mode == 'replace_first':
                    replace(suggestions[0])
                elif mode == 'show_list':
                    show_list(text, suggestions)
            except IndexError:
                pass