import argparse

from vtorch.agent.worker import Worker


def execute(args: argparse.Namespace) -> None:
    _worker = Worker(cpu_only=args.cpu_only, gpus=args.gpus)
    _worker.execute(
        task_id=args.id,
        log_level=args.log_level,
        disable_monitoring=args.disable_monitoring,
        require_queue=args.require_queue,
        log_file=args.log_file,
        standalone_mode=args.standalone_mode,
        clone=args.clone,
        projects_path=args.projects_path,
        venv_name=args.venv_name,
    )


def daemon(args: argparse.Namespace) -> None:
    _worker = Worker(debug=args.debug, cpu_only=args.cpu_only, gpus=args.gpus)
    _worker.daemon(
        queues=args.queues,
        venv_names=args.venv_names,
        projects_paths=args.projects_paths,
        log_level=args.log_level,
        foreground=args.foreground,
        detached=args.detached,
        order_fairness=args.order_fairness,
        child_report_tags=args.child_report_tags,
        use_owner_token=args.use_owner_token,
        standalone_mode=args.standalone_mode,
        services_mode=args.services_mode,
        uptime=args.uptime,
        downtime=args.downtime,
        stop=args.stop,
        create_queue=args.create_queue,
        status=args.status,
        gpus=args.gpus,
        dynamic_gpus=args.dynamic_gpus,
    )


def main() -> None:
    common_args_parser = argparse.ArgumentParser(add_help=False)
    common_args_parser.add_argument("--standalone-mode", action="store_true")
    common_args_parser.add_argument(
        "--log-level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL"]
    )
    common_args_parser.add_argument("--gpus", type=str)
    common_args_parser.add_argument("--cpu-only", action="store_true")

    # execute single / daemon
    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers()
    execute_parser = subparsers.add_parser("execute", parents=[common_args_parser])
    execute_parser.add_argument("--id", type=str, required=True)
    execute_parser.add_argument("--log-file", type=str, required=False)
    execute_parser.add_argument("--disable-monitoring", action="store_true")
    execute_parser.add_argument("--projects-path", type=str, default=".")
    execute_parser.add_argument("--venv-name", type=str, default="venv")
    execute_parser.add_argument("--require-queue", action="store_true")
    execute_parser.add_argument("--clone", action="store_true")
    execute_parser.set_defaults(func=execute)

    daemon_parser = subparsers.add_parser("daemon", parents=[common_args_parser])
    daemon_parser.add_argument("--foreground", action="store_true")
    daemon_parser.add_argument("--queues", nargs="+", required=True)
    daemon_parser.add_argument("--projects-paths", nargs="+", required=True)
    daemon_parser.add_argument("--venv-names", nargs="+", default=None)
    daemon_parser.add_argument("--debug", action="store_true")
    daemon_parser.add_argument("--order-fairness", action="store_true")
    daemon_parser.add_argument("--services-mode", action="store_true")
    daemon_parser.add_argument("--child-report-tags", nargs="+")
    daemon_parser.add_argument("--create-queue", action="store_true")
    daemon_parser.add_argument("--detached", action="store_true")
    daemon_parser.add_argument("--stop", action="store_true")
    daemon_parser.add_argument("--dynamic-gpus", action="store_true")
    daemon_parser.add_argument("--uptime", type=str)
    daemon_parser.add_argument("--downtime", type=str)
    daemon_parser.add_argument("--status", action="store_true")
    daemon_parser.add_argument("--use-owner-token", action="store_true")
    daemon_parser.set_defaults(func=daemon)

    arguments = parser.parse_args()
    arguments.func(arguments)


if __name__ == "__main__":
    main()
