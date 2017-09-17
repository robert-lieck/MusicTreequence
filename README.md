# MusicTreequence
MusicTreequence is a Python library to code music. It provides an abstraction layer on top of [Sonic Pi](http://sonic-pi.net/), which in turn is a front end to [SuperCollider](http://supercollider.github.io/). MusicTreequence produces Ruby code that can be processes by Sonic Pi, that is, if you want to listen to what you've coded with MusicTreequence you have to install Sonic Pi, which is cross-platform, free and open source.
## Listen to the Music
For an easy start
 1. code some music (have a look at the small [Tutorial](./Tutorial.ipynb) for a start) and write it to a file called 'song.rb'
 1. open [main.rb](./main.rb) in Sonic Pi
 1. adapt the path to 'song.rb' to the directory where you've just saved your music
 1. run [main.rb](./main.rb)
## Look at the Music
In the future I might add some simple export to music scores using [music21](http://web.mit.edu/music21/). For this to work you have to install music21 and [MuseScore](https://musescore.org/en) (also cross-platform, free and open source) and set up music21 to use MuseScore for producing visual output by executing the following Python code:
```
from music21 import *
us = environment.UserSettings()
us.create()  # create config file
print(us.getSettingsPath())  # location of config file
us['musescoreDirectPNGPath'] = '/usr/bin/mscore'  # output of `which mscore`
```
You can test whether it's working by executing something like this
```
converter.parse("tinynotation: 3/4 CC#16 d8 f g16 a g f# 4/4 c4 d8 f g16 a g f#").show()
```
## The Name
This library is called MusicTreequence because some aspects in music have a sequential nature (such as voice leading) and some are rather structured like trees (such as harmony). Since we somehow need a combination of both...you know...
