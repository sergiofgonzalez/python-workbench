# Simple Rendering Library
> A simplistic rendering library using OpenGL and PyGame as the backend engine.


## Notes

An enhancement over [09: RenderGL (no cam)](../09-rendergl-no-cam/) that includes support for passing a function to the `draw_model` function that returns a time-based matrix to perform the animation.

When passing that function, the corresponding animation is activated by default.

Note also that matrix-based animation requires being able to multiply the given time-based matrix by each of the face's vectors. Because of that, a symbolic link has established between the `mat` library hosted on [matlib](../10_mat-lib/) in the root of the project:

```bash
$ pwd
~/.../python-workbench/part_2-math/02_mini-projects/11-rendergl-no-cam-matrix

$ ln -s ../10_mat-lib/mat/ mat
```


Because this version is based on the no-cam version of RenderGL is supports the same set of interactive actions:

+ Press x, y, z to rotate the scene about the corresponding axis. They act like on/off switches.
+ press key up, key down to translate the scene in the y axis
+ press key up, key down to translate the scene in the y axis