#!/usr/bin/env python3
from asap3 import print_version
from asap3 import LennardJones
from asap3.io import Trajectory
from asap3.md.velocitydistribution import MaxwellBoltzmannDistribution
from asap3.md.verlet import VelocityVerlet
from ase.parallel import parprint, world
from ase import units
import time, os, numpy
from warnings import simplefilter
from main import run_program


def main():
    # Supress some warnings that get very frequent in parallel output
    simplefilter(action='ignore', category=FutureWarning)

    run_program()


if __name__ == '__main__':
    main()
