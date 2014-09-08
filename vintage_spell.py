import sublime_plugin, sublime
import hunspell 

class VintageSpellCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self.dictionary = hunspell.HunSpell('./en_US.dic', './en_US.aff')
        self.selection = ''
        self.word = None
        self.suggestions = []

    def run(self, edit, mode):
        region = self.view.sel()[0]
        self.word = self.view.word(region)
        text = self.view.substr(self.word)

        if self.dictionary.spell(text) == True:
            return
        else:
            self.suggestions = self.dictionary.suggest(text)
            if mode == 'replace_first':
                self.selection = self.suggestions[0]
                self.replace(edit)
            elif mode == 'show_list':
                self.show_list(text, self.suggestions)

    def replace(self, edit):
        self.view.replace(edit, self.word, self.selection)
            
    def show_list(self, text, suggestions):
        v = self.view.window().new_file()
        v.set_name('Change "%s" to:' % text)
        v.set_scratch(True)

        edit = v.begin_edit()
        for i, suggestion in enumerate(suggestions):
            v.insert(edit, v.text_point(i, 0), suggestion + '\n')
        v.end_edit(edit)

        v.window().show_input_panel(
            'Type number and <Enter> (empty cancels): ', '', 
            self.on_done, None, self.on_cancel)

    def on_cancel(self):
        sublime.active_window().run_command('close')
        
    def on_done(self, input):
        try:
            self.selection = self.suggestions[int(input) - 1]
            edit = self.view.begin_edit()
            self.replace(edit)
            self.view.end_edit(edit)
        except:
            pass
        sublime.active_window().run_command('close')
