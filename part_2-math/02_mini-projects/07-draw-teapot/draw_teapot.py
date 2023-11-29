"""Main program: execute this program to draw the teapot
"""
from teapot import load_triangles
from draw_model import draw_model

if __name__ == "__main__":
    draw_model(load_triangles())
