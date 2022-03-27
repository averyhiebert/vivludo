''' This script contains some examples of how to use the
various automata classes and image renderers in the vivludo package. 

It contains several functions, each of which is a standalone
example of how to create and render images or animations of a particular
cellular automaton. The "Wirewold" example in particular is the most useful
for understanding the NonTotalistic class, which is the most general of the
provided classes of automaton.

This script also serves as a rough replacement for regression testing.'''

from vivludo.render import *
from vivludo.automata import *

import numpy as np

def life():
    ''' Create a gif of Conway's Game of Life, demonstrating use of
    the vivludo.automata.LifeLike class.'''
    gol = LifeLike("B3/S23",edges="wrap")
    # Start with 100x100 randomized grid
    gol.set_state(np.random.randint(0,2,100*100).reshape(100,100))
    # Render a gif of 500 generations, using default colours (green on black)
    make_gif(gol,500,colors=2,frame_duration=0.1,
        filename="images/life.gif",scale=2)

def wireworld():
    ''' Create a gif of a simple circuit (a clock and two diodes) in
    the Wire World automaton, demonstrating use of the 
    vivludo.automata.NonTotalistic class. '''

    # Define a function which takes a 3x3 array, representing a cell and its
    # neighbourhood, as inputs, and returns the new state for the cell:
    def rule(input_array):
        # 0 = dead, 1 = conductor, 2 = electron head, 3 = electron tail
        cell = input_array[1,1]
        if cell == 0:
            return 0
        elif cell == 2:
            return 3
        elif cell == 3:
            return 1
        else:
            heads = [x for x in input_array.reshape(9) if x == 2]
            elec = len(heads) == 1 or len(heads) == 2
            return 2 if elec else 1
    # Pass this update rule function into the NonTotalistic constructor:
    ww = NonTotalistic(rule,base=4,nb="moore",edges="fixed",edge_fill=0)
    # Define an initial state for the automaton (a simple clock & diodes):
    pattern = [[0,0,0,0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,1,1,0,0,0],
              [0,0,2,0,1,1,0,1,1,1,1],
              [0,3,0,1,0,0,1,1,0,0,0],
              [0,1,0,1,0,0,0,0,0,0,0],
              [0,1,0,1,0,0,0,0,0,0,0],
              [0,1,0,1,0,0,0,0,0,0,0],
              [0,1,0,1,0,0,0,0,0,0,0],
              [0,1,0,1,0,0,0,0,0,0,0],
              [0,1,0,1,0,0,1,1,0,0,0],
              [0,0,1,0,1,1,1,0,1,1,1],
              [0,0,0,0,0,0,1,1,0,0,0],
              [0,0,0,0,0,0,0,0,0,0,0]]
    ww.set_state(pattern)
    # Specify some colours and render a gif of 16 generations of the pattern:
    colours = [[0,0,0],[255,255,255],[255,0,0],[255,180,0]]
    make_gif(ww,16,colours,
        frame_duration=0.1, filename="images/wireworld.gif",scale=10)
    # (Note the use of "scale=10" to display each cell 
    #  as a square 10 pixels by 10 pixels, since this is a fairly small
    #  pattern, and pixel art does not look good when magnified in many
    #  modern image viewers)

def brians_brain():
    ''' Create a gif of the Brian's Brain automaton, further demonstrating
    use of the vivludo.automata.NonTotalistic class. '''
    def rule(input_array):
        # 0 = dead, 1 = alive, 2 = dying
        cell = input_array[1,1]
        if cell == 1:
            return 2
        if cell == 2:
            return 0
        living_neighbours = len([x for x in input_array.reshape(9) if x == 1])
        return 1 if living_neighbours == 2 else 0
    bb = NonTotalistic(rule,base=4,nb="moore",edges="wrap",edge_fill=0)
    bb.set_state(np.random.randint(0,3,100*100).reshape(100,100))
    make_gif(bb,300,colors=3, frame_duration=0.1, 
        filename="images/brians_brain.gif", scale=2)

def rule110():
    ''' Run Wolfram's Rule 110 from simple initial conditions
    for 200 generations, and create an image of the result,
    demonstrating use of the vivludo.automata.ECA class'''
    r110 = ECA(110, edges="wrap")
    r110.set_state([0]*199 + [1])
    # Create a list of 200 successive states.
    states = list(r110.n_generations(200))
    # Render as an image
    save_image(np.array(states),colors=[[255,255,255],[0,0,0]],
        filename="images/rule110.png",scale=2)

def anneal():
    ann = LifeLike("B4678/S35678",edges="wrap")
    ann.set_state(np.random.randint(0,2,500*500).reshape(500,500))
    for i in range(50):
        ann.step()
    save_image(ann.copy_state(),colors=2,filename="images/anneal.png")

def majority_vote():
    vote = LifeLike("B5678/S45678",edges="wrap")
    vote.set_state(np.random.randint(0,2,500*500).reshape(500,500))
    for i in range(100):
        vote.step()
    save_image(vote.copy_state(),colors=[[100,0,120],[150,0,170]],
        filename="images/majority_vote.png")

if __name__=="__main__":
    print("Creating Life gif")
    life()
    print("Creating Wire World gif")
    wireworld()
    print("Creating Brian's Brain gif")
    brians_brain()
    print("Creating Rule 110 image")
    rule110()
    print("Creating Anneal image")
    anneal()
    print("Creating Majority Vote image")
    majority_vote()

