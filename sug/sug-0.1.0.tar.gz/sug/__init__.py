def sug(
    name: str,
    working_dir: str,
    exec_start: str,
    bin_path: str,
    user: str,
    group: str,
    description: str = "",
    service_type: str = "simple",
):
    return f"""[Unit]
Description={description}
ConditionPathExists={bin_path}
After=network.target

[Service]
Type=simple
User={user}
Group={group}
LimitNOFILE=1024
Restart=on-failure
RestartSec=10
startLimitIntervalSec=60

WorkingDirectory={working_dir}
ExecStart={exec_start}

# make sure log directory exists and owned by syslog

StandardOutput=journal
StandardError=journal
SyslogIdentifier={name}

[Install]
WantedBy=multi-user.target
"""
