# Vector 2D library
> Refactoring the Vector 2D library to accommodate both graphing and Math functions


## Vector 2D Graphing library

A library to draw simple figures such as points, segments, polygons, and  arrows in the 2D plane using Matplotlib as the backend.
The library exposes classes for the figures, an enumeration for the common colors, and a function `draw` to render the figures.

| Class | Constructor example | Description |
| :---- | :------------------ | :---------- |
| `Polygon` | `Polygon(*vectors)` | Draws a polygon whose vertices (plural of vertex) are represented by the given list of vectors. |
| `Points` | `Points(*vectors)` | Represents a list of points (i.e., dots), one at each of the input vectors. |
| `Arrow` | `Arrow(tip)`<br>`Arrow(tip, tail)` | Draws an arrow from the origin to the `tip` vector, or from the `tail` vector to the `tip` vector if `tail` if given. |
| `Segment` | `Segment(start, end)` | Draws a line segment from the start to the vector end. |

