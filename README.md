# Vivludo
Vivludo is a library for working with cellular automata in Python.

There are many other PyPI packages for cellular automata, but most of them
were not quite what I was looking for, so I decided to make my own.  It's not
really intended to be a "product", but since I was making it anyways I figured
there was no reason not to release it.  I can't guarantee support, 
documentation, and so on.

This package uses a reasonably fast implementation based on convolution
(not as fast as whatever Golly uses, though). 
I think it might be possible to modify it for GPU acceleration 
(using PyTorch or something), but I haven't tried that.

*Vivludo* is Esperanto for "Life Game", in reference to Conway's Game of Life,
which is one of the most well-known cellular automata.

## Installation

`pip install vivludo`

Requires Python 3.5 or greater.

## Usage
Some usage examples can be found in the `examples` directory.  
I may eventually add actual documentation, but for now there's just the
docstrings in the source code.

## Licence
This package is released under the MIT licence, as described in `LICENCE.txt`.
