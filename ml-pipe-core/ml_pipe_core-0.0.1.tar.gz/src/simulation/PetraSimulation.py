from src.ml_pipe_core.adapter.PetraSimulationAdapter import PetraSimulationAdapter
from optics_sim import OpticsSimulation
from MachineService import MachineService

if __name__ == "__main__":
    machine_adapter = PetraSimulationAdapter()
    sim = MachineService('petra_III_sim', machine_adapter, OpticsSimulation(machine_adapter))
    sim.init_local()
