import sublime_plugin 
import sublime
import hunspell 

class VintageSpellCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self.dictionary = hunspell.HunSpell('./en_US.dic', './en_US.aff')
        # sublime.log_commands(True)

    def run(self, edit, mode):
        region = self.view.sel()[0]
        word = self.view.word(region)
        text = self.view.substr(word)

        if self.dictionary.spell(text) == True:
            return
        else:
            suggestions = self.dictionary.suggest(text)
            if mode == 'replace_first':
                self.replace(edit, word, suggestions[0])
            elif mode == 'show_list':
                self.show_list(word, suggestions, self.view.window())
            # tessst

    def replace(self, edit, word, suggestion):
        self.view.replace(edit, word, suggestion)

    def show_list(self, word, suggestions, window):
        list_view = window.new_file()
        list_view.set_name('Change "%s" to:' % self.view.substr(word))
        for suggestion in suggestions:
            #region = sublime.Region(0, 10)
            print suggestion