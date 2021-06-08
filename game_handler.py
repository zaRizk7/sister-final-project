import game_lib as gl
from mpi4py import MPI

comm = MPI.COMM_WORLD

# Get rank and size of initialized programs
rank, size = comm.Get_rank(), comm.Get_size()
