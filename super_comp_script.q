#!/bin/bash
#
#SBATCH -J CDIO-job
#SBATCH -A liu-compute-2024-33
#SBATCH --reservation devel
#SBATCH -t 02:30:00
#SBATCH -N 1
#SBATCH -n 32
#SBATCH --exclusive
#
export NSC_MODULE_SILENT=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS1

for i in {0..3}
do
    j=$(bc <<<"scale=2;0.01")
    k=$(bc <<<"scale=2;$i*$j*32")
    mpprun python3 supercomp_main.py -slurm -simulation_method Interface -lattice_interpolation -film_alloy_ratio $k -sc_film_alloy_ratio_offset $j -sc
done
#time mpprun python3 md_parallel.py

echo "job completed"
