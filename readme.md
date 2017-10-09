# Oddyssey

The project is an open world roguelike game using [PYGUSES](https://github.com/KodeWorker/PYGUSES). The goal is to create a vivid procedually-generated open-world environment for player to interact. And the world keep on simulation while the game progresses.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* [python](https://www.python.org/) - 3.6 or higher
* [pygame](https://www.pygame.org/) - 1.9.3 or higher
* [numpy](http://www.numpy.org/) - 1.11.3 or higher
* [PYGUSES](https://github.com/KodeWorker/PYGUSES) - 0.0.2-alpha or higher

### Installing

```
git clone --recursive https://github.com/KodeWorker/Oddyssey.git
cd Oddyssey
pip install -r requirements.txt
```

## Running the Game

Oddyssey source code is in /src/GameManager. The PYGUSES module is in /src/PYGUSES.

### Source code test

Run the main python script.

```
cd src
python /main.py
```

## Contributing

Please read [contributing.md](contributing.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/KodeWorker/PYGUSES/tags). 

## Authors

* **Shin-Fu Wu** - *Initial work* - [KodeWorker](https://github.com/KodeWorker)

See also the list of [contributors](https://github.com/KodeWorker/Oddyssey/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [license.md](license.md) file for details

## Acknowledgments

* This project is inspired by [Doryen](http://roguecentral.org/doryen/)'s work on [libtcod](https://bitbucket.org/libtcod/libtcod).
* Thanks to **Billie Thompson** - [PurpleBooth](https://github.com/PurpleBooth) for her document templates.
* Thanks to [Dwarf Fortress](http://www.bay12games.com/dwarves/) and [Cataclysm: Dark Days Ahead](http://en.cataclysmdda.com/) for hundreds of happy hours.
* Amit's [Red Blob Games](http://www.redblobgames.com/) provides details on many procedual-generation algorithms.
