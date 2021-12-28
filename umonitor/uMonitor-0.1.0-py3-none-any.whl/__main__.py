from .uMonitor import uMonitor as uMonitor

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
