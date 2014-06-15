#!/usr/bin/python2
# -*-coding:utf-8 -*
"""

    main.py

    Entry point of the simulation. Its only job is to run the simulation.

"""


from simulator import Simulator


if __name__ == '__main__':
    sim = Simulator()
    sim.on_execute()
