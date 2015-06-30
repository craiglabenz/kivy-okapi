## Okapi

#### What it is
A library to build grid-based games using Kivy 1.9


#### Installation

Installing packages with Kivy is a joy because you cannot use virtual environments (assuming you use the Kivy package installer). Kivy creates its own unique snowflake environment, then provides a `kivy` command-line utility that heavily modifies your `PYTHONPATH` before ultimately launching the python interpreter. Thus, virtual environments are off the table, as none of their packages can be imported after using `kivy`.

1. [Download the Kivy installer](http://kivy.org/docs/installation/installation.html) and use it to install Kivy.

1. Next, install `Okapi` from PyPI, but be sure to install it where Kivy is willing to look on your machine. On Mac OS X, that is here: `/Applications/Kivy.app/Contents/Resources/venv/lib/python2.7/site-packages`

    ```sh
    pip install kivy-okapi -t /Applications/Kivy.app/Contents/Resources/venv/lib/python2.7/site-packages
    ```

#### Launching an `Okapi` App

Once `Okapi` is installed where Kivy is willing to look, you can simply navigate into any game folder and run `kivy main.py` like normal, and all Okapi libraries will be available.
