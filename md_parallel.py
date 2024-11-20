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

# Supress some warnings that get very frequent in parallel output
simplefilter(action='ignore', category=FutureWarning)

#cpulayout = (2, 2, 2)    # 8 cores in 2*2*2 grid
cpulayout = "auto"       # Just figure it out...

# Print Asap version
if world.rank == 0:
    print_version(1)

# parprint only print on the rank=0 process
parprint("Simulation started: {0}\n".format(time.ctime()))

# Read the atoms distributed over the processes.
atoms = Trajectory("initial.traj").get_atoms(-1, cpulayout)
nAtoms = atoms.get_number_of_atoms()
parprint("Distribution on CPU cores: {0}\n".format(str(atoms.nCells)))
calculator = LennardJones([18], [0.010323], [3.40], rCut=-1,
                          modified=True)
atoms.set_calculator(calculator)

MaxwellBoltzmannDistribution(atoms, 40 * units.kB)

dyn = VelocityVerlet(atoms, 1.0 * units.fs)
traj = Trajectory("argon.traj", "w", atoms)
dyn.attach(traj.write, interval=100)

step = 0
def printenergy(a=atoms):
    """Function to print the potential, kinetic and total energy"""
    global step
    epot = a.get_potential_energy()
    ekin = a.get_kinetic_energy()
    epot_per_atom = epot / len(a)
    ekin_per_atom = ekin / len(a)
    parprint(step,
          "Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  "
          "Etot = %.3feV" % (epot_per_atom, ekin_per_atom,
          ekin_per_atom / (1.5 * units.kB),
          epot_per_atom + ekin_per_atom))
    step+=100

dyn.attach(printenergy, interval=100)
printenergy()
dyn.run(1000)
