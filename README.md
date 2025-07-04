<img width=400 alt="BOLDswimsuite logo" src="https://github.com/jacobchausse/BOLDswimsuite/blob/main/boldswimsuite_logo.png">

# Installation Guide

## Getting Access

This public repository only contains the lessons, examples and documentation for the package, not the source code. To gain access to the code, please fill out the [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSdgYc8M5KIoXqs_O89c0_Wwa25sbXWC_4JJk7L7tPJ4yH2oqw/viewform) with your institutional/workpace email that is linked to your github account so we can add you to the private repository.

## Requirements
- Python 3.10.X

## Installing BOLDswimsuite

Using the command line, navigate to the location of the package. The directory should have "pyproject.toml" in it (and this very file, "README.md").

The package can be installed either with or without the dependencies required to run the lessons.

To install with the lesson and display dependencies (for new users that want to do the lessons), execute the following command (from the location of the package):
```
pip install ".[lessons,display]"
```

To install without the lesson or display dependencies, execute the following command (from the location of the package):
```
pip install .
```

This will install all the dependencies to the Python installation. To test if everything installed properly, from the same directory in the command line, execute the following: 

```
python .\examples\3D-ANA-MC_script.py
```

This should run a short simulation and output an image with three plots, showing the different signals.

## Starting the Lessons

The lessons are made with Jupyter notebook, and so must be opened with it (requires the "lessons" dependencies). First open Jupyter by executing the following command in the command line (in the same directory as the last two commands):

```
jupyter notebook
```

This will open Jupyter in a web browser, where you will be greeted with the UI showing the current directory. From there enter the "lessons" directory. The lessons should be listed, they can be opened in the browser. Lesson 0 briefly explains how to use Jupyter notebooks, so anyone unfamiliar with them should start there. Otherwise lesson 1 covers the first topic on BOLDswimsuite.
