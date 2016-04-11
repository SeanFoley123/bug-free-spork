# Symbiosis

**Sean Foley, Kaitlyn Keil, Apurva Raman**

**Software Design, Spring 2016**

Symbiosis is a game in which you play as a blobby orphan baby trying to find a family to accept it. Using powers granted to you by a mushroom symbiote, traverse levels and make decisions to meet your goal.

## Dependencies
This project uses the math, sys, and pygame libraries. Make sure these are installed before playing the game.

## Modules
To play, run the file game_base2.py. This imports the modules Spores, LivingThings, Terrain, and Room. These contain the classes needed to run the game.
- Spores contains the classes for the thrown spores, such as decomposition and ledge-creation.
- Terrain contains the classes for the platforms and surfaces and obstacles.
- LivingThings contains the classes for the player and creatures that move.
- Room contains and constructs the levels, and imports the above modules.

## Keybindings
Use the arrow keys to move. Spacebar throws spores. Up arrow key allows you to jump. Don't hit the enemy, try to survive!