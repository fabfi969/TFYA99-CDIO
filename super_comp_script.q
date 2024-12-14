#!/bin/bash
#
#SBATCH -J CDIO-job
#SBATCH -A liu-compute-2024-33
#SBATCH --reservation devel
#SBATCH -t 00:05:00
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --exclusive
#
export NSC_MODULE_SILENT=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS1

j=$(bc <<<"scale=2;0.1")
mpprun python3 supercomp_main.py -slurm -lattice_constant 2 -sc_lattice_offset $j -sc

#time mpprun python3 md_parallel.py

echo "job completed"
