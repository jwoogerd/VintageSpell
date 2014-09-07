import sublime_plugin, sublime
import hunspell 

class VintageSpellCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self.dictionary = hunspell.HunSpell('./en_US.dic', './en_US.aff')
        #sublime.log_commands(True)

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
                suggestion = self.show_list(edit, text, suggestions)
                self.replace(edit, word, suggestion)
            # oneness
            
    def replace(self, edit, word, suggestion):
        self.view.replace(edit, word, suggestion)

    def show_list(self, edit, text, suggestions):
        v = self.view.window().new_file()
        v.set_name('Change "%s" to:' % text)
        v.set_scratch(True)
        v.settings().set('is_spell', True)

        for i, suggestion in enumerate(suggestions):
            v.insert(edit, v.text_point(i, 0), suggestion + '\n')

        v.insert(edit, v.text_point(len(suggestions), 0), 
            '\nType number and <Enter> (empty cancels): ')

        return suggestions[0]


class VintageSpellEventListener(sublime_plugin.EventListener):
    def on_close(self, view):
        if view.settings().get('is_spell') == True:
            print 'close'

