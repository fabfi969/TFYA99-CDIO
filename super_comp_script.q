#!/bin/bash
#
#SBATCH -J testjob
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
export OMP_NUM_THREADS=1

time mpprun python3 main.py

echo "job completed"
