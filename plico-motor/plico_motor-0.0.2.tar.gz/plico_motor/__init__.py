from plico_motor.utils.constants import Constants


def _getDefaultConfigFilePath():
    from plico.utils.config_file_manager import ConfigFileManager
    cfgFileMgr = ConfigFileManager(Constants.APP_NAME,
                                   Constants.APP_AUTHOR,
                                   Constants.THIS_PACKAGE)
    return cfgFileMgr.getConfigFilePath()


defaultConfigFilePath = _getDefaultConfigFilePath()


def motor(hostname, port):

    from plico_motor.client.motor_client import MotorClient
    from plico.rpc.zmq_remote_procedure_call import ZmqRemoteProcedureCall
    from plico.rpc.zmq_ports import ZmqPorts
    from plico.rpc.sockets import Sockets

    rpc = ZmqRemoteProcedureCall()
    zmqPorts = ZmqPorts(hostname, port)
    sockets = Sockets(zmqPorts, rpc)
    return MotorClient(rpc, sockets)
