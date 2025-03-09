# Installation Guide

1. Getting the package from Github
2. Installing Python
3. Installing Poetry
4. Creating the Python Virtual Environment
5. Starting the Lessons

## 1. Getting the package from Github

### Using Github Desktop
Using Github Desktop (https://desktop.github.com/) is the easiest way to get access to the repository for those without experience with git. 

Once installed, the following steps can be followed to add the package to your computer:
1. Log In to Github Desktop.
2. At the top left (under file), click on the "Current Repository" button.
3. Change the repository to "BOLDswimsuite".
4. Clone the repository.
>Note: Make sure to know where the Github folder is on your computer, this is where the package is located and we will need it during the creation of the Python virtual environment.

## 2. Installing Python

Download Python 3.10.4 at the following link:
https://www.python.org/downloads/release/python-3104/

- For Windows use the "Windows installer (64-bit)", which is the recommended option.
- For Mac, use the "macOS 64-bit universal2 installer".

## 3. Installing Poetry

Install Poetry 1.6.1 using the instructions at the following link:
https://python-poetry.org/docs/#installation 

If you have multiple versions of python installed on your computer, you may need to change which version Poetry uses with:

```
poetry env use /full/path/to/python
```

(replacing the last part with the full path to the Python 3.10.4 executable). More detailed instructions: https://python-poetry.org/docs/managing-environments/#switching-between-environments.

## 4. Creating the Python Virtual Environment

This will install all the dependencies which are required for the project, and create a Python virtual environment from which we can run Python files and Jupyter notebooks (for the lessons).

Using the command line, navigate to the location of the package (where it has been cloned either from Github Desktop or git). The directory should have the "poetry.lock" and "pyproject.toml" in it (and this very file, "README.md").

Execute the following command: 
```
poetry install --with analysis
``` 
This will install all the dependencies required and create the virtual environment. The `--with analysis` portion includes the optional dependencies to run the lessons, generate plots and package results.
> Note: Whenever a different version or branch of the package is used, it is important to run this command again, as the dependencies may change.

To test if everything installed properly, from the same directory in the command line, execute the following: 

```
poetry run python ./examples/3D-ANA-MC_script.py
```

This should run a short simulation and output an image with three plots, showing the different signals.

## 5. Starting the Lessons

The lessons are made with Jupyter notebook, and so must be opened with it (it has been installed as part of the Poetry dependencies). First open Jupyter by executing the following command in the command line (in the same directory as the last two commands):

```
poetry run jupyter notebook
```

This will open Jupyter in a web browser, where you will be greeted with the UI showing the current directory. From there enter the "lessons" directory. The lessons should be listed, they can be opened in the browser. Lesson 0 briefly explains how to use Jupyter notebooks, so anyone unfamiliar with them should start there. Otherwise lesson 1 covers the first topic on BOLDswimsuite.
