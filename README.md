# spike_removal

![build](https://github.com/pmdias/spike_removal/workflows/build/badge.svg?branch=master)

Tool used to remove spikes from polygons.

## Description

This tool can be used to remove spikes from input geometries stored in
`geopackage` format. This is done by parsing the input geometry and evaluating
each set of three contigous vertices against an evaluating strategy and
removing from the output geometry the vertices that fail to pass the test.

### Spike definition

The tool will consider a target vertex to be a spike if the following criteria
is met:

* The angle formed by the edges that meet at the target vertex is smaller than
a certain angle (default is 1º);

* Both edges that connect the target vertex to its neighbors vertices have at
least a minimum length (default is 100 000 meters, i.e., 100 km);

When a vertex meets both of the criteria, it is removed from the geometry and
will not be included in the output geometry.


## Example

![example](https://github.com/pmdias/spike_removal/blob/master/docs/example.png?raw=true)


## Installation

This tool single external dependency is [geopandas](https://geopandas.org/). The
dependency can be installed simply by running

```
$ pip install geopandas
```

Installation of the `spike_removal` tool can be done in either of two ways.
The first one requires cloning this repository and the installation is done
from a local copy

```
$ git clone https://github.com/pmdias/spike_removal.git
$ cd spike_removal
$ python setup.py install
```

As an alternative, you can install from git using `pip` if you wish to manage
the installation using `pip`

```
$ pip install git+https://github.com/pmdias/spike_removal.git
```


## Usage

Simple example of using this tool to process a file:

```
$ spike_removal -o output.gpkg input.gpkg
```

For more details run `spike_removal --help`:

```
Usage: spike_removal [OPTIONS] FILENAME

  A command-line tool used to remove spikes from polygons stored in
  Geopackage format.

Options:
  --angle FLOAT      Maximum angle, in degrees, used to evaluate spikes.
                     Defaults to 1.0º.

  --distance FLOAT   Minimum distance, in meters, used to evaluate spikes.
                     Defaults to 100 000m

  -o, --output TEXT  Name of the output destination file  [required]
  --help             Show this message and exit.
```

The tool accepts three diferent input arguments:

* `--angle`: The maximum angle, in degrees, that will be used to evaluate
triplets of vertices. If the triplet being evaluated forms an angle greater
than the value of `angle`, that triplet will never be marked as a spiked. The
value of `angle` defaults to 1.0º if not specified;

* `--distance`: The minimum distance, in meters, that one of the edges of the
triplet being evaluated must have for that triplet to be tested as a spike.
The value of `distance` defaults to 100 000 meters if not specified;

* `--output`: The output path where the processed geometry will be saved to;


## Details

The following diagram provides a more detailed explanation of the internals
of this tool.

![diagram](https://github.com/pmdias/spike_removal/blob/master/docs/spike_removal_diagram.svg?raw=true)
