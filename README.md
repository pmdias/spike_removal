# spike_removal

![build](https://github.com/pmdias/spike_removal/workflows/build/badge.svg?branch=master)

Tool used to remove spikes from polygons.

## Description

Brief description of the tool


## Installation

Installation guide


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


## Diagram

![diagram](https://github.com/pmdias/spike_removal/blob/master/docs/spike_removal_diagram.svg?raw=true)
