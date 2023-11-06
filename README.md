# NINE LIVES

a python/pygame game created by during [Bodensee GameJam 2023](https://spieleentwicklung-bodensee.de/gamejam2023/) by msmr, rosobe and zeha

we chose the topic "Death is not the End", featuring a little cat that lives on as a ghost when dying, changing its abilities.


## how to run:

    python game.py
or

    python3 game.py

depending on your python setup

requirements:

    python3
    pygame 2.0 or higher




## your mission:

- move the cat and eat fish (the normal looking ones)
- push boxes to block light (you'll need that later when dead)
- when all normal fish are eaten, die by touching a mad robovac
- go on as a ghost cat and eat fishbones
- don't get touched by light as a ghost, but wander through walls instead
- when all fish are eaten (both normal ones and bones), the level is complete

the game has 9 levels, so you'll experience a whole cat life cycle.

## controls:

- press space to start
- use arrow keys to move around
- press ESC to pause and then R to retry a level, Q to quit, or ESC to unpause
- NOTE: there is an edit mode inside, which is a bit quirky to use (it's just there for us developers). you can access/leave the edit mode with TAB, load levels by pressing 1-9, save levels by pressing S, move the cursor with cursor keys, set/delete objects using various letters and keys (e.g. b=box, #=wall, k=candle, space=floor)
