from distutils.core import setup
import py2exe

setup(
    name = 'BiokteriiAnnealing',
    description = 'Simulated Annealing Biokterii',
    version = '0.1',

    windows = [
                  {
                      'script': 'main.py',
                      #'icon_resources': [(1, "handytool.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      'packages':'encodings',
                      'includes': 'cairo, pango, pangocairo, atk,  gio, gobject, pygtk ',
                  }
              },
)
