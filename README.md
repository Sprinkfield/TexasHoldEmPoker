# Texas HoldEm Poker (low budget version)

Experience the beauty of poker with incredibly human-like AI! This game promises an unforgettable experience. Try it out for yourself now!

## Requirements for launch
You need Python 3.8+ and the following modules: [numpy](https://pypi.org/project/numpy/) and [pygame](https://pypi.org/project/pygame/).

If you don't have the these package, use pip (in a terminal or command line) to install them:
```bash
pip install numpy pygame
```


## Launching
Go to the game folder through the terminal and run the launch.py file:

Windows:
```bash
python .\launch.py
```
Linux/MacOS:
```bash
python3 .\launch.py
```

## Customizable AI
Currently there are 2 versions of the AI:

1. **ai_alpha** - Neural Network (unpredictable, **can(NOT)** bluff)
2. **ai_beta** - Logical Algorithm (usually predictable, **can** bluff)

You can switch between them by changing the 4th line of code in launch.py.

## Customizable Player Profile
You can change your nickname in the settings menu.

To change your profile picture by uploading it to the *images/avatars/* folder with the name *player.png*
