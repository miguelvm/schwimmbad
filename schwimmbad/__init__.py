# coding: utf-8
"""
Contributions by:
- Peter K. G. Williams
- Júlio Hoffimann Mendes
- Dan Foreman-Mackey

Implementations of four different types of processing pools:

    - MPIPool: An MPI pool.
    - MultiPool: A multiprocessing for local parallelization.
    - SerialPool: A serial pool, which uses the built-in ``map`` function

"""

# Standard library
import sys
import logging
log = logging.getLogger(__name__)
_VERBOSE = 5

from .multiprocessing import MultiPool
from .serial import SerialPool
from .mpi import MPIPool
from .jl import JoblibPool

def choose_pool(mpi=False, processes=1, **kwargs):
    """
    Chooses between the different pools.
    """

    if mpi:
        if not MPIPool.enabled():
            raise SystemError("Tried to run with MPI but MPIPool not enabled.")

        pool = MPIPool(**kwargs)
        if not pool.is_master():
            pool.wait()
            sys.exit(0)

        log.info("Running with MPI on {} cores".format(pool.size))
        return pool

    elif processes != 1 and MultiPool.enabled():
        log.info("Running with MultiPool on {} cores".format(processes))
        return MultiPool(processes=processes, **kwargs)

    else:
        log.info("Running with SerialPool")
        return SerialPool(**kwargs)
