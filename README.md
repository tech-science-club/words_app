App with purpose to ease learning languages. 

Main idea is to help to learn single words, phrases, get its translation. Was decided to implement  deep_translator library as tranlation engine.
Treating of text is occuring with the help of re library.
I tried to envolve as much as possible conponents of Kivy 1.1.1 GUI.
To not overload attantion of user, I have tryed to make as much as possible design solution and stopped on idea of having main interface with 4 buttons, 
which might lead us to 4 screens: screen with lists of words, screen with possbility to add words from sentences, from articles and setting screen.
To treat text, to sort out separated words out of punctuation signs, digits, spaces here have been used regular expressions method.

Work description of the 1st screen is here in video. It contains a list of word sets, pressing on a line we go to words list together with its translation.
Pressing on it we will go to cards mode, which helps us to memorise words, its translation and swipe it to the right/ left side

https://github.com/tech-science-club/words_app/assets/130900888/d39a9266-aa75-46a3-9d57-f414ed93ef66

2nd screen gives us possibilities to add words from sentenses. We can call a pop up menu, put in a text line whole sentence and chose target words, add them 
to word set, save it into memory

https://github.com/tech-science-club/words_app/assets/130900888/a87accb0-579d-410d-857b-68052aca238d

3d screen allows us to treat whole article, snipped of a text. We may put it into text field, select intresting words for as just taping on it, press button and add it into 
word set

https://github.com/tech-science-club/words_app/assets/130900888/91aa575a-6a75-4f6e-999b-00e7b9c06b3d

NavigationDrawer work is here. We can open menu which contains lists, clicking on its lines, we can go directly to there

https://github.com/tech-science-club/words_app/assets/130900888/5404bd38-e1b3-44cd-b908-881f31914d1a


