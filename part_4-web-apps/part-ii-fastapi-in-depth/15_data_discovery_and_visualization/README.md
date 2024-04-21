# Data Discovery and Visualization

## Handling CSV data and its variants

The following snippet illustrates how to read a pipe-separated values (PSV) file using the `csv` package:

```python
def read_csv(filename: str) -> list[list[str]]:
    """Read a CSV file and return a list of tuples."""
    with open(filename, encoding="utf-8") as file:
        info = [row for row in csv.reader(file, delimiter="|")]
        return info


if __name__ == "__main__":
    data = read_csv(sys.argv[1])
    # Print the first 5 rows of the CSV file
    for row in data[0:5]:
        print(row)
```

## Displaying table data using [`tabulate`](https://github.com/astanin/python-tabulate)

The following snippet illustrates how to display data in a tabular format using [`tabulate`](https://github.com/astanin/python-tabulate) open source module.

```python
from tabulate import tabulate

def read_csv(filename: str) -> list[list[str]]:
    """Read a CSV file and return a list of tuples."""
    with open(filename, encoding="utf-8") as file:
        info = [row for row in csv.reader(file, delimiter="|")]
        return info


if __name__ == "__main__":
    data = read_csv(sys.argv[1])
    print(tabulate(data[0:5], headers="firstrow"))
```

## Pandas

The following snippet illustrates how to read a CSV/PSV file and return a Pandas dataframe:

```python
import pandas as pd


def from_csv_get_df(filename: str) -> pd.DataFrame:
    """Read a CSV file and return a pandas DataFrame."""
    return pd.read_csv(filename, sep="|")


if __name__ == "__main__":
    data = from_csv_get_df(sys.argv[1])
    print(data.head(5))
```

## Chart/Graph Packages

The following table lists the most popular packages for graphical data displays and an opinionated description:

| Library | Description |
| :------ | :---------- |
| [Matplotlib](https://matplotlib.org/) | Extensive but requires some work to get beautiful results. |
| [Plotly](https://plotly.com/python/) | Similar to Matplotlib and Seaborn, with an emphasis on interactive graphs. |
| [Dash](https://dash.plotly.com/) | Dashboard tool based on Plotly. |
| [Seaborn](https://seaborn.pydata.org/) | Built on top of Matplotlib and offering a higer-level interface, but with less graph types. |
| [Bokeh](https://bokeh.org/) | Interactive visualization tool for modern browsers.<br>Integrates well with JavaScript and supports visualization of very large datasets. |

The following snippet illustrates how you can use Plotly Express to return a histogram from a FastAPI application:

```python
...
from collections import Counter

import plotly.express as px
from fastapi.responses import Response

...

router = APIRouter(prefix="/creature")


@router.get("/plot-histogram")
def plot_histogram():
    creatures = service.get_all()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    counts = Counter(creature.name[0] for creature in creatures)
    y = {letter: counts.get(letter, 0) for letter in letters}
    fig = px.histogram(
        x=list(letters),
        y=y,
        title="Creature Names by First Letter",
        labels={"x": "Creature Initial", "y": "Initials"},
    )
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")
```

## Map Packages

The following table lists few popular packages for maps and geovisualization.

| Library | Description |
| :------ | :---------- |
| [PyGIS](https://pygis.io/docs/a_intro.html) | Spatial programming package with good tutorials. |
| [PySAL](https://pysal.org/) | Spatial data analysis library. |
| [Cartopy](https://scitools.org.uk/cartopy/docs/latest/) | Geo data analysis. |
| [Folium](https://python-visualization.github.io/folium/latest/) | Map visualization integrated with [leafleft.js](https://leafletjs.com/) library. |
| [Python Client for Google Maps](https://github.com/googlemaps/google-maps-services-python) | Official client for Google Maps service. |
| [Geemap](https://geemap.org/) | Python package for interactive geospatial analysis and visualization with Google Earth Engine. |
| [Geoplot](https://residentmario.github.io/geoplot/index.html) | Extension of Maplotlib and Cartopy for maps. |
| [GeoPandas](https://geopandas.org/en/stable/) | Pandas extension for geographical data. |
| [ArcGIS and ArcPy](https://pro.arcgis.com/en/pro-app/latest/arcpy/main/arcgis-pro-arcpy-reference.htm) | Geoprocessing tooling in Python. |

The following snippet illustrates how to plot a geo map using Plotly express:

```python
...
import country_converter as coco
import plotly.express as px
...
router = APIRouter(prefix="/creature")


@router.get("/map")
def plot_map():
    creatures = service.get_all()
    iso2_codes = set(creature.country for creature in creatures)
    iso3_codes = coco.convert(names=list(iso2_codes), to="ISO3")
    fig = px.choropleth(
        locationmode="ISO-3",
        locations=iso3_codes,
    )
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")
```