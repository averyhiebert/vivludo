''' Defines a Cellular Automaton class and a couple of likely subclasses.'''
import re
import warnings
# Ignore benign warning from scipy
warnings.filterwarnings("ignore", message="numpy.dtype size changed")

import numpy as np
from scipy.signal import convolve2d

import vivludo.utils as utils

class ConvCA():
    ''' Fairly fast way of implementing many 2d automata, using convolution.
    
    The automaton is specified using a kernel and an update array.  To
    compute one generation of the automaton, the array representing the
    automaton state is convolved with the given kernel to give an
    intermediate array, and then each cell's intermediate value is used to 
    look up its final value in the update array.'''
    def __init__(self, update_array, kernel, edges="wrap",edge_fill=0):
        ''' Specify the precomputed update array and the integer kernel.'''
        # Should probably do some type checking.
        if edges not in ["wrap","fixed"]:
            raise ValueError("Invalid edge mode: %s" % edges)
        if edges == "wrap":
            self.convolve_boundary = "wrap"
        elif edges == "fixed":
            self.convolve_boundary = "fill"
        self.update_array = update_array
        self.kernel = kernel
        self.edges = edges
        self.edge_fill = edge_fill
        self.cell_array = None

    def step(self):
        ''' Perform one step of the automaton. '''
        self.cell_array = self.update_array[convolve2d(self.cell_array,
            self.kernel, boundary=self.convolve_boundary,
            fillvalue=self.edge_fill, mode="same")]

    def set_state(self, cell_array):
        '''Set the state of the cellular automaton to match the given array.'''
        self.cell_array = np.copy(cell_array)

    def copy_state(self):
        return np.copy(self.cell_array)

    def n_generations(self, n=-1):
        ''' A generator, possibly useful for live animation etc.
        It will return successive states of the cellular automaton, 
        up to n states.  The first state returned will be the (unchanged)
        initial state.

        Set n=-1 (or other negative number) to run infinitely. '''
        count = 0
        while count < n or n < 0:
            if count > 0:
                # Don't step for the first iteration.
                self.step()
            if n >= 0:
                # Don't increase count if set to n=-1
                count += 1
            yield self.copy_state()

class LifeLike(ConvCA):
    ''' Fast implementation of Lifelike Cellular Automata. 
    
    Also supports "larger-than-life" and weighted variants of life (in theory),
    although I haven't really tested these use cases.'''
    @classmethod
    def parse(cls, rule_string,r,weights):
        '''Given a rule string, return the corresponding
        internal weight array, and precomputed rule array.
        
        rule_string can also include a list of 2 lists, with the first
        representing values for which a cell is born, and the second
        representing values for which a cell survives.'''
        # Calculate kernel
        if not weights:
            size = 2*r + 1 # The size of the neighbourhood
            kernel = np.ones(size*size,dtype=int).reshape(size,size)
            kernel[r,r] = 0
        else:
            # Should probably add checks for shape and dtype
            # Flip weights, since they'll get flipped back during convolution.
            kernel = np.flip(weights)
            kernel[r,r] = 0
        weight_sum = kernel.sum()
        kernel[r,r] = weight_sum + 1

        # If rule_string is already an array of integers, assume it's valid
        if len(rule_string) == 2 and type(rule_string[0]) == type([]):
            live, survive = rule_string
        # Otherwise, parse the B/S rule
        else:
            m = re.search("^[bB]?(\d*)/[sS]?(\d*)$",rule_string)
            if not m:
                raise ValueError("Invalid rule: %s",rule_string)
            live = [int(char) for char in m.group(1)] # Born
            survive = [int(char) for char in m.group(2)] # Survive
        living = live + [weight_sum + 1 + i for i in survive]
        update_array = np.array([1 if i in living else 0 for 
            i in range(2*(weight_sum+1))])

        return update_array, kernel
            
    def __init__(self, rule_string, edges="wrap",edge_fill=0,r=1,weights=None):
        ''' Rule_string should be in the "B/S" format 
        (e.g. "B3/S23", "3/23", or [[3],[2,3]] for Conway's Game of Life).
        
        A radius can optionally be specified, or an array of integer weights
        can be specified (this overrides the radius param) allowing both
        "weighted" variations of life, as well as neighbourhoods other than
        the Moore neighbourhood. The array of weights must be square, and the
        centre weight will be disregarded.'''
        update_array, kernel = LifeLike.parse(rule_string,r,weights)
        ConvCA.__init__(self,update_array,kernel,
            edges=edges,edge_fill=edge_fill)
        
class ECA(ConvCA):
    ''' Implementation of "Wolfram's Rule [n]" elementary cellular 
    automata. '''
    def __init__(self,n,edges="wrap",edge_fill=0):
        ''' Create the elementary cellular automaton corresponding to the
        integer n, 0 <= n <= 255. '''
        if type(n) != int:
            raise TypeError("Not a valid rule: %s" % n)
        if n > 255 or n < 0:
            raise ValueError("Not a valid rule: %s" % n)

        # Define the appropriate "Wolfram's rule n"
        update_array = np.array([int(digit) 
            for digit in reversed(format(n,"08b"))])
        kernel = np.array([[1,2,4]]) # Note reversed order
        update_array = np.array(update_array)
        ConvCA.__init__(self,update_array,kernel,
            edges=edges,edge_fill=edge_fill)

    # Note: need to override set_state and copy_state to handle the conversion
    #  from 1d to 2d and vice-versa.
    def set_state(self, cell_array):
        ''' Set the state of the cellular automaton to match the 
        given array (and convert from 1d to 2d).'''
        self.cell_array = np.copy([cell_array])

    def copy_state(self):
        ''' Return current state (first convert to 1d) '''
        return np.copy(self.cell_array[0])


class NonTotalistic(ConvCA):
    ''' General purpose non-totalistic automaton class. '''

    @classmethod
    def parse_kernel(cls,base,nb):
        ''' nb is the type of neighbourhood to use. '''
        nb = nb.lower()
        if nb not in utils.nb_patterns:
            raise ValueError("Invalid neighbourhood type: %s" % nb)
        exponentiated = (base*utils.nb_patterns[nb])**utils.nb_exponents[nb]
        # Note: multiplying by the pattern a second time is needed since,
        #  according to python, 0**0 = 1.
        return utils.nb_patterns[nb]*exponentiated

    @classmethod
    def parse_rule(cls,rule,base,nb):
        ''' nb is the type of neighbourhood to use. '''
        if callable(rule):
            return utils.func_to_update_array(rule, base, nb)
        else:
            # We make the dangerous assumption that this is an update array.
            return rule

    def __init__(self,rule,base=2,nb="moore",edges="wrap",edge_fill=0):
        '''Define a non-totalistic cellular automaton.

        "base" is the number of possible states. "nb" is the type of
        neighbourhood to use.  "rule" is an update function.

        Note that the rule is precomputed ahead of time, so probabilistic
        rules will not work.  Note also that the time efficiency of the update
        rule only matters when initializing, since outcomes are precomputed
        in advance.  However, this means that the space needed for a
        base b totalistic cellular automaton using the Moore neighbourhood
        is O(b^9), or O(b^5) if using the Von Neumann neighbourhood, so be
        careful not to use too large of a base.
        '''
        kernel = NonTotalistic.parse_kernel(base,nb)
        update_array = NonTotalistic.parse_rule(rule,base,nb)
        ConvCA.__init__(self,update_array,kernel,
            edges=edges,edge_fill=edge_fill)
        
