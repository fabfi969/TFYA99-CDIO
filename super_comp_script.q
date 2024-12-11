#!/bin/bash
#
#SBATCH -J CDIO-job
#SBATCH -A liu-compute-2024-33
#SBATCH --reservation devel
#SBATCH -t 00:25:00
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --exclusive
#
export NSC_MODULE_SILENT=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS1

for i in {1..50}
do
    j=$(bc<<<"scale=2;2+$i*0.1")
    python3 main.py -film_lattice $j -simulation_method Interface -slurm
done

#time mpprun python3 md_parallel.py

echo "job completed"
