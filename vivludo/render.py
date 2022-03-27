''' Some tools for rendering images and gifs of cellular automata. 

Most of these functions require the imageio package.'''
import imageio
import numpy as np

# Define an okayish palette to use by default.
# We assume 0 is some sort of "dead" state, so it's black.
#  Then use green, cyan, blue, magenta, red, yellow, and white as necessary.
#  (If the base gets any higher, just reuse white.)
default_palette = [[0,0,0],[0,255,0],[0,255,255],[0,0,255],
    [255,0,255],[255,0,0],[255,255,0],[255,255,255]]

def get_palette(num_colors):
    ''' Return a palette of a set number of colours (up to 8 distinct
    colours, after which white will be used to fill out the rest
    of the list). 

    Returns a list of 3-element lists representing rgb values.'''
    if num_colors < len(default_palette):
        return default_palette[:num_colors]
    else:
        deficit = num_colors - len(default_palette)
        return default_palette + [[255,255,255]]*deficit

def scale_image(ar,n):
    '''Given a 2d numpy array, return a version of the array created by
    replacing each cell with an n by n square of cells.

    This is useful if you don't want each cell of your cellular automaton
    picture to appear larger than 1 pixel. '''
    return ar.repeat(n,axis=0).repeat(n,axis=1)

def make_gif(ca,num_frames,colors=8,frame_duration=0.1, filename="./ca.gif",
        reverse_loop=False,subrectangles=False,palette_size=256,scale=1):
    ''' Render a gif of the given cellular automaton ca.
    
    Filename must have .gif extension.'''
    if type(colors) == int:
        colors = np.array(get_palette(colors),dtype=np.uint8)
    else:
        colors = np.array(colors,dtype=np.uint8) # unit8 for gif
    frame_list = [colors[f] for f in ca.n_generations(num_frames)]
    if reverse_loop:
        # Make it play forwards & backwards, creating a perfect loop in time.
        frame_list = frame_list + list(reversed(frame_list))[1:-1]
    if scale != 1:
        frame_list = [scale_image(f,scale) for f in frame_list]
    imageio.mimsave(filename, frame_list,duration=frame_duration,
        subrectangles=subrectangles,palettesize=palette_size)

def save_image(grid,colors=8, filename="./ca.png", scale=1):
    ''' Render a still image of a grid of integers, representing each
    integer by a pixel using the given color palette.  The file type will be
    determined by the extension of the given filename.'''
    if type(colors) == int:
        colors = np.array(get_palette(colors),dtype=np.uint8)
    else:
        colors = np.array(colors,dtype=np.uint8)
    img = colors[grid]
    if scale != 1:
        img = scale_image(img,scale)
    imageio.imwrite(filename, img)
