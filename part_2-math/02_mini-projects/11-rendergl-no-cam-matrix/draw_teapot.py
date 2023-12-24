"""Basic example that draws the canonical Utah Teapot"""
from math import cos, sin

from rendergl import draw_model, load_triangles


if __name__ == "__main__":
    # Default view
    # draw_model(load_triangles())

    # View from (0, 0, 0), default is (0, 0, -25)
    # draw_model(load_triangles(), glTranslatef_args=(0.0, 0.0, -25))

    # View from (-5, -5, -5) (to the right, up, further away)
    # draw_model(load_triangles(), glTranslatef_args=(-1.0, -1.0, -5.0))

    # Tilt 30° about the z-axis
    # draw_model(load_triangles(), glRotatef_args=(30, 0, 0, 1))

    # Tilt 30° about the x-axis
    # draw_model(load_triangles(), glRotatef_args=(30, 1, 0, 0))

    # Tilt 30° about the y-axis
    # draw_model(load_triangles(), glRotatef_args=(30, 0, 1, 0))

    def time_based_rotation_matrix(t):
        seconds = t / 1000
        return (
            (cos(seconds), 0, -sin(seconds)),
            (0, 1, 0),
            (sin(seconds), 0, cos(seconds)),
        )
    draw_model(
        load_triangles(), get_matrix=time_based_rotation_matrix
    )
