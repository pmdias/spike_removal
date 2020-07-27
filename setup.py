#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Python installation script
"""
from setuptools import find_packages, setup


setup(
    name="spike_removal",
    version="0.0.1",
    license="MIT License",
    description="Tool used to remove spikes from polygons in geospatial data",
    long_description="""
        Tool used to remove spikes from polygons in geospatial data
    """,
    author="Pedro Dias",
    author_email="pedrodias.miguel@gmail.com",
    url="https://github.com/pmdias/spike_removal",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Utilities"
    ],
    project_urls={
        "Issue Tracker": "https://github.com/pmdias/spike_removal/issues",
    },
    keywords=[
        "spike_removal", "geometry", "geographic", "geopandas",
    ],
    python_requires=">=3.6",
    install_requires=[
        "geopandas>=0.8.1",
    ],
    entry_points={
        "console_scripts": [
            "spike_removal = spike_removal.cli:main",
        ]
    },
)
