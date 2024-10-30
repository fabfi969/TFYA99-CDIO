"""Demonstrates molecular dynamics with constant energy. Is called by main.py"""

from asap3 import EMT, LennardJones, Trajectory
from ase import units
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet


def calcenergy(a):  # store a reference to atoms in the definition.
    """Function to calculate the potential, kinetic and total energy."""
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    etot = epot + ekin
    return (epot, ekin, etot)


def run_md(args, input_data):

    # Set up a crystal
    atoms = FaceCenteredCubic(
        directions=input_data["atoms"]["directions"],
        symbol=input_data["atoms"]["materials"][0],
        size=(
            input_data["atoms"]["x_size"],
            input_data["atoms"]["y_size"],
            input_data["atoms"]["z_size"],
        ),
        pbc=input_data["atoms"]["pbc"],
    )

    # Describe the interatomic interactions with the Effective Medium Theory
    if args.simulation_method == "EMT":
        atoms.calc = EMT()
    elif args.simulation_method == "LennardJones":
        atoms.calc = LennardJones(
            input_data["lennard_jones"]["atomic_number"],
            input_data["lennard_jones"]["epsilon"],
            input_data["lennard_jones"]["sigma"],
            input_data["lennard_jones"]["r_cut"],
            modified=input_data["lennard_jones"]["modified"],
        )

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=input_data["temperature_K"])

    # We want to run MD with constant energy using the VelocityVerlet algorithm.
    dyn = VelocityVerlet(atoms, input_data["time_step"])
    traj = Trajectory(input_data["trajectory_file_name"], "w", atoms)
    # dyn.attach(traj.write, interval=input_data["trajectory_interval"]) #TODO check what this line does

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        """Function to print the potential, kinetic and total energy."""
        epot, ekin, etot = calcenergy(a)
        print(
            "Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  "
            "Etot = %.3feV" % (epot, ekin, ekin / (1.5 * units.kB), etot)
        )

    # Now run the dynamics
    dyn.attach(printenergy, interval=input_data["trajectory_interval"])
    printenergy()
    dyn.run(1000)
