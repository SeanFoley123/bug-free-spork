# Symbiosis

**Sean Foley, Kaitlyn Keil, Apurva Raman**

**Software Design, Spring 2016**

Symbiosis is a platform game in which you play as a blobby orphan baby trying to find a family to accept it. Using powers granted to you by a mushroom symbiote, traverse levels and make decisions to meet your goal. 
Game Site: https://sites.google.com/site/symbiosisthegame/home
Game Drive: https://drive.google.com/open?id=0Byeh9J0R89gxbTJKakREYWRnbTA

## Dependencies
This project uses the math, sys, collections, numpy and pygame libraries. Make sure these are installed before playing the game.

## Modules
To play, run the file game_base2.py. This imports the modules Spores, LivingThings, Terrain, and Room. These contain the classes needed to run the game.
- Spores contains the classes for the thrown spores, such as decomposition and ledge-creation.
- Terrain contains the classes for the platforms and surfaces and obstacles.
- LivingThings contains the classes for the player and creatures that move.
- Room contains and constructs the levels, and imports the above modules.
- HUD contains classes for dialogue and stat bars
- Menu creates a menu
- Intro contains Video/cutscenes
- game_base2 displays and runs the game using a Controller and View class

## Getting Started
To download the code to run Symbiosis, open https://github.com/SeanFoley123/bug-free-spork/archive/master.zip in a browswer.

## Usage
Run from game_base2.py. This should open a pygame window, beginning with a cutscene. Press 'space' to advance through this cutscene. The game will then begin.

### Keybindings
Use the left and right arrow keys to move. Spacebar throws spores; change which type using 'e' (grows ledges) and 'q' (kills and destroys objects). The down arrow key lets you eat mushrooms to regain health. 't' allows you to talk to your sybiotic mushroom friend. 'p' brings up the pause menu. Don't hit the enemy, try to survive!

## Credit
http://programarcadegames.com/python_examples/show_file.php?file=platform_jumper.py for basic platforming code

## License
MIT License

Copyright (c) 2016 Sean Foley, Kaitlyn Keil, Apurva Raman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
