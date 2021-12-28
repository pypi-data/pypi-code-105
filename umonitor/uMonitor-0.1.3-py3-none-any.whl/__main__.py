from .uMonitor import *
from .uMonitor import uMonitor as uMonitor

def sig_handler(signal, frame):
    print("signal: ", signal)
    sys.exit(0)

def catch_signals(signals: set):
    catchable = signals - { signal.SIGKILL, signal.SIGSTOP }
    for sig in catchable:
        signal.signal(sig, sig_handler)

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            '''Setup the environment and run processes
            based on the given configuration file'''
        )
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="CONFIG",
        default="config.json",
        help=(
            '''json configuration file on
            how to run your processes'''
        )
    )
    arguments = parser.parse_args()
    return arguments

def main():
    arguments = parse_args()
    with uMonitor(arguments.CONFIG) as p:
        p.run()

if __name__ == "__main__":
    catch_signals({signal.SIGINT})
    main()
