from src.ml_pipe_core.adapter.PetraMachineAdapter import PetraMachineAdapter
from MachineService import MachineService

if __name__ == "__main__":
    machine_adapter = PetraMachineAdapter()
    sim = MachineService('petra_III_machine', machine_adapter, None)
    sim.init_local()
