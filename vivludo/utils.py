''' Define some functions useful for cellular automata.'''
import numpy as np
import itertools

# Define some constants describing the various neighbourhoods available
nb_sizes = {
    "moore": 9,
    "von neumann": 5,
    "extended": 9
}

nb_patterns = {
    "moore": np.array([[1,1,1],
                      [1,1,1],
                      [1,1,1]]),
    "von neumann": np.array([[0,1,0],
                            [1,1,1],
                            [0,1,0]]),
    "extended": np.array([[0,0,1,0,0],
                         [0,0,1,0,0],
                         [1,1,1,1,1],
                         [0,0,1,0,0],
                         [0,0,1,0,0]])
}

# Note: everything is flipped, since it will be flipped back during convolution.
nb_exponents = {
    "moore": np.flip([[0,1,2],
                      [3,4,5],
                      [6,7,8]]),
    "von neumann": np.flip([[0,0,0],
                            [1,2,3],
                            [0,4,0]]),
    "extended": np.flip([[0,0,0,0,0],
                         [0,0,1,0,0],
                         [2,3,4,5,6],
                         [0,0,7,0,0],
                         [0,0,8,0,0]])
}

def padded_base_b(x,b,length):
    ''' 
    Convert the integer x to its base b representation, padding it with
    zeros if the result is less than the specified length.'''
    if x == 0:
        return [0]*length
    if x < 0:
        raise RuntimeError("x should not be negative")
    digits = []
    while x:
        digits.append(x % b)
        x = x // b
    if len(digits) < length:
        digits =  digits + [0]*(length - len(digits))
    return digits

# Note: In theory every non-totalistic function that we can handle should have
#  an integer encoding, but I'm not sure this is
#  any more convenient than just working with update arrays themselves.
#
#  Nonetheless, here are some functions for using these encodings.
#  Use at your own risk.
#
#  (Note: at the moment these may not match with the conventions used by
#   Golly and other cellular automaton tools to encode non-totalistic cellular
#   automata)
def int_to_update_array(i,base,nb):
    ''' Convert from an integer to an update array for a non-totalistic
    rule in the specified base using the specified neighbourhood '''
    return padded_base_b(i,base,base**nb_sizes[nb]) 

def update_array_to_int(arr,base):
    ''' Convert from an update array (in the specified base) to the
    corresponding integer encoding.
    
    Note: in some cases, this will be veeeeeerrrry slllloooooooow.'''
    coefficient = 1
    total = 0
    for x in arr:
        total += coefficient*x
        coefficient = coefficient * base
    return total

# This is the actually important function.
def func_to_update_array(func, base, nb):
    ''' Convert a function describing an update rule
    to its array representation (i.e. precompute the result for
    all possible inputs).
    
    The function should take a 3x3 array (in the case of the Moore 
    neighbourhood) or an array of 5 or 9 elements (in the case of Von Neumann
    and Extended Von Neumann).
    
    For Von Neumann, the array [a,b,c,d,e] corresponds to:
        a
      b c d
        e
    For extended Von Neumann, the array [a,b,c,d,e,f,g,h,i] corresponds to:
        a
        b
    c d e f g
        h
        i
    '''
    nb = nb.lower()
    size = nb_sizes[nb]
    possibilities = itertools.product(range(base),repeat=size)
    result = []
    for poss in possibilities:
        poss = np.flip(poss) # Must be reversed to match intended pattern
        if nb=="moore":
            poss = poss.reshape(3,3)
        result.append(func(poss))
    return np.array(result)
