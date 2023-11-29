"""
__init__.py for the rendergl package which provides rendering utilities.
"""
from rendergl.camera import Camera, default_camera
from rendergl.draw_model import draw_model
from rendergl.teapot import load_triangles
from rendergl.transforms import (
    compose,
    polygon_map,
    rotate_x_by,
    rotate_y_by,
    rotate_z_by,
    scale_by,
    translate_by,
)

__all__ = [
    "default_camera",
    "Camera",
    "draw_model",
    "load_triangles",
    "compose",
    "polygon_map",
    "rotate_x_by",
    "rotate_y_by",
    "rotate_z_by",
    "scale_by",
    "translate_by",
]
