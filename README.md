###VintageSpell
---
A Sublime Text package for emulating Vi/Vim spelling keyboard shortcuts.

####Installation
---

Go to your Sublime Text `Packages` directory and clone this 
repository: `https://github.com/jwoogerd/VintageSpell.git`

####Use
---
`z1` replaces word under the cursor with the first dictionary suggestion.
`z=` suggests correctly spelled words for the word under the cursor.

This package uses [Pyhunspell](https://code.google.com/p/pyhunspell/), a set of Python bindings for the Hunspell spellchecker engine.

TODO:
 - fix window closing on canceled suggestion