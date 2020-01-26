# Tabletop Helper
A tabletop assistant for Dungeons and Dragons 5e

This tabletop assistant is built for Dungeons and Dragons 5e and for assisting players in character creation, rolling, and encounter management. Curretly, it features auto-calculating modifier fields, saving and loading character files, opening multiple characters at once, simple initiative tracking, and quick searching using two D&D REST APIs.

## Future Improvements

Future releases of this application will include the following:

* Dice rolling widget
* Rolling stats with an associated button click
* Customizable color for rolling
* Beautification of saved JSON file for ease of reading
* Dungeon master tools for encounter planning
* Potential 3D dice roller using Qt3D

## Dependencies

This project relies on several built-in Python libraries, but it requires the following libraries to be installed:

* requests
* PyQt5

## Running

The application can be run through Python and the path to TabletopHelper.py

## Why PyQt

Although Qt is a C++ UI framework, PyQt is a wrapper for the Python language. Native Qt through C++ will always be faster and more responsive, especially considering Python's overhead, but Python is an extremely easy language to prototype in. Thus the language provides an easy way to show a proof of concept without the need for much setup. Translation from Python to C++ is not planned, but the PyQt wrapper is almost one-to-one with Qt, and therefore, such a process would not be too difficult.
