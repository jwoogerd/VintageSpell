import sublime_plugin, sublime
import hunspell 

class VintageSpellCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        path = sublime.packages_path()
        self.dictionary = hunspell.HunSpell(
        path + '/Language - English/en_US.dic',
        path + '/Language - English/en_US.aff')

    def run(self, edit, mode):
        region = self.view.sel()[0]
        word = self.view.word(region)
        text = self.view.substr(word)

        def replaceWith(selection):
            self.view.replace(edit, word, selection)

        def show_list(text, suggestions):
            def on_done(index):
                if index > -1:
                    replaceWith(suggestions[index])

            self.view.window().show_quick_panel(
                suggestions, on_done, sublime.MONOSPACE_FONT)

        if self.dictionary.spell(text) == False:
            try:
                suggestions = self.dictionary.suggest(text)
                selection = suggestions[0]
                if mode == 'replace_first':
                    replaceWith(selection)
                elif mode == 'show_list':
                    show_list(text, suggestions)
            except IndexError:
                sublime.status_message('No spelling suggestions') 
