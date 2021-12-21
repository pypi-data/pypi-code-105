#
#  (c) Copyright 2021 Micro Focus or one of its affiliates.
#

from vcli.util.static_params import (
    VAAS_MODULES, AWS_INSTANCE_TYPES,
    SUPPORTED_VERTICA_VERSIONS,
    VALID_NODES_NUMBERS, VALID_TASK,
    CRON_ACTION, TOGGLE_ACTION,
    VALID_REPORT_NAME, VALID_REPORT_RANGE,
    IDLE_SHUTDOWN_TIME
)
from vcli.constant import (
    MAX_ATTEMPTS_DEFAULT,
    MIN_DB_NAME_LENGTH, MAX_DB_NAME_LENGTH,
    MIN_DNS_NAME_LENGTH, MAX_DNS_NAME_LENGTH,
    MAX_CRON_NAME_LENGTH
)


# Note List
DB_NAME_NOTE = f"""
The database name must consist of {MIN_DB_NAME_LENGTH} to {MAX_DB_NAME_LENGTH}
alpha-numeric characters and start with a letter.
"""
SUBCLUSTER_NAME_NOTE = F"""
The subcluster name must consist of {MIN_DB_NAME_LENGTH} to {MAX_DB_NAME_LENGTH}
alpha-numeric characters and start with a letter.
"""
CRON_NAME_NOTE = f"""
The maximum cron job name length is {MAX_CRON_NAME_LENGTH} characters.
"""
DNS_NAME_NOTE = f"""
The DNS name must consist of {MIN_DNS_NAME_LENGTH} to {MAX_DNS_NAME_LENGTH}
alpha-numeric characters and start with a letter.
"""


class HelpMessage:
    ##########
    ## VCLI ##
    ##########
    vcli_header = """
    Vertica Command Line Interface (VCLI) is a tool to manage Vertica Accelerator databases.
    """

    #############
    ## Profile ##
    #############
    profile = """
    Use a specific profile from the credentials file (default path:
    "~/.vcli/credentials"). If you don't specify a profile, VCLI defaults to the
    'default' profile when communicating with Vertica Accelerator services.
    """

    ############################
    ## Login & Logout Service ##
    ############################
    login_header = """
    Log in to Vertica Accelerator.
    """

    logout_header = """
    Log out from Vertica Accelerator.
    """

    ####################
    ## Config Service ##
    ####################
    config_header = """
    Configure VCLI to access Vertica Accelerator.
    """

    # config: set command
    config_set = """
    Setup the user configuration file. 
    If this command is run with no arguments, you will be prompted for configuration values.
    You can configure a named profile using the "--profile" argument.  
    If your config file does not exist, the VCLI will create it for you. 
    The default location of vcli config file is "~/.vcli/config".
    """

    set_username = """
    The VaaS username of the user.
    """
    set_password = """
    The VaaS password of the user.
    """
    set_client_id = """
    The OKTA client id of the application.
    """
    set_auth_endpont = """
    The OKTA authentication endpoint to authenticate the user.
    """
    set_service_endpoint = """
    The OA service endpoint to make the request.
    """
    set_max_attempts = f"""
    The maximum number of retry attempts to make for the request.
    By default this value is {MAX_ATTEMPTS_DEFAULT}.
    """
    set_verify_ssl = f"""
    If set to false, the request will not check ssl certificate on service endpoint.
    By default this value is true.
    """

    ######################
    ## Database Service ##
    ######################
    database_header = """
    Manage the Database.
    """

    # database: create command
    database_create = """
    Create a new database.
    """

    create_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    create_password = """
    The password for the database.
    The password must consist of 8 to 30 upper-case,
    lower-case, numeric, and special characters.
    """
    create_nodes = f"""
    The number of primary cluster nodes for the database.
    Valid values: {VALID_NODES_NUMBERS.list()}
    """
    create_region = """
    The region of the database.
    For example: 'us-east-1'
    """
    create_availability_zone = """
    The availability zone of the database.
    For example: 'us-east-1a'
    """
    create_instance_type = f"""
    The instance type of the database.
    Valid values: {AWS_INSTANCE_TYPES.list()}
    """
    create_external_access_cidr_block = """
    The IPv4 external access CIDR block(s) of the database, which acts as a whitelist
    for a range of IP addresses that can access the database as a client. For example, 
    the CIDR block 192.0.2.0/24 allows clients to connect from 192.0.2.0 through 192.0.2.255. 
    Separate multiple CIDR blocks with a comma: 192.0.2.0/24,192.0.2.0/32
    """
    create_vertica_version = f"""
    The AMI version of the Vertica database.
    Valid values: {SUPPORTED_VERTICA_VERSIONS.list()}
    """

    # database: list command
    database_list = """
    View a list of the databases and their properties.
    """
    list_brief = """
    If set to true, only brief list of database will be returned containing only database names.
    Valid values: ['True', 'False']
    """

    # database: get command
    database_get = """
    View details of a particular database and its subclusters.
    """
    get_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """

    # database: start command
    database_start = """
    Start the database.
    """
    start_name = f"""
    The name of the database.
    Note:{DB_NAME_NOTE}
    """

    # database: stop command
    database_stop = """
    Stop the database.
    """
    stop_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """

    # database: hibernate command
    database_hibernate = """
    Hibernate the database.
    """
    hibernate_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """

    # database: revive command
    database_revive = """
    Revive the database.
    """
    revive_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    revive_availability_zone = f"""
    The availability zone for the database.
    For example: 'us-east-1a'
    """
    revive_instance_type = f"""
    The instance type for the database.
    Valid values: {AWS_INSTANCE_TYPES.list()}
    """
    revive_external_access_cidr_block = """
    The IPv4 external access CIDR block(s) of the database, which acts as a whitelist
    for a range of IP addresses that can access the database as a client. For example, 
    the CIDR block 192.0.2.0/24 allows clients to connect from 192.0.2.0 through 192.0.2.255. 
    Separate multiple CIDR blocks with a comma: 192.0.2.0/24,192.0.2.0/32
    """
    revive_vertica_version = f"""
    The ami version of vertica.
    Valid values: {SUPPORTED_VERTICA_VERSIONS.list()}
    """

    # database: drop command
    database_drop = """
    Drop an existing database.
    """
    drop_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """

    # database: increase command
    database_increase = """
    Increase the number of nodes for the database.
    """
    increase_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    increase_module = f"""
    The subcluster_id to increase the node count.
    Valid values: {VAAS_MODULES.list()}
    """
    increase_nodes = f"""
    The node count to increase for the targeted module.
    Valid values: {VALID_NODES_NUMBERS.list()}
    """

    # database: decrease command
    database_decrease = """
    Decrease the number of nodes for the database.
    """
    decrease_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    decrease_module = f"""
    The subcluster_id to decrease the node count.
    Valid values: {VAAS_MODULES.list()}
    """
    decrease_nodes = f"""
    The node count to decrease for the targeted module.
    Valid values: {VALID_NODES_NUMBERS.list()}
    """

    # database: rescale command
    database_rescale = """
    Change the instance type of the nodes.
    """
    rescale_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    rescale_module = f"""
    The subcluster_id to rescale the instance type.
    Valid values: {VAAS_MODULES.list()}
    """
    rescale_instance_type = f"""
    The rescale targeted instance type for the database.
    Valid values: {AWS_INSTANCE_TYPES.list()}
    """
    rescale_subcluster_name = f"""
    The name of the subcluster.
    {SUBCLUSTER_NAME_NOTE}
    """

    # database: upgrade command
    database_upgrade = """
    Upgrade a database.
    """
    upgrade_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    upgrade_vertica_version = f"""
    The ami version of vertica.
    Valid values: {SUPPORTED_VERTICA_VERSIONS.list()}
    """

    # database: update-network-config command
    database_update_network_config = """
    Update the external access CIDR block.
    """
    update_network_config_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    update_network_config_external_access_cidr_block = """
    The IPv4 external access CIDR block(s) of the database, which acts as a whitelist
    for a range of IP addresses that can access the database as a client. For example, 
    the CIDR block 192.0.2.0/24 allows clients to connect from 192.0.2.0 through 192.0.2.255. 
    Separate multiple CIDR blocks with a comma: 192.0.2.0/24,192.0.2.0/32
    """
    update_network_config_enable_ssh = """
    Boolean value to enable/disable ssh access to Vertica database instances.
    """

    #############################
    ## Database Config Service ##
    #############################
    database_config_header = """
    Manage the Database Configuration.
    """

    # database-config: idle-shutdown command
    database_config_idle_shutdown = """
    The database configuration for idle-shutdown.
    """

    # database-config: idle-shutdown list command
    database_config_idle_shutdown_list = """
    List the idle-shutdown configuration for a particular database.
    """
    database_config_idle_shutdown_list_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    database_config_idle_shutdown_list_enabled = """
    Filter result by the enable flag. All schedule configures will be returned if no flag is specified.
    """

    # database-config: idle-shutdown update command
    database_config_idle_shutdown_update = """
    Update the idle-shutdown configuration for a particular database.
    """
    database_config_idle_shutdown_update_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    database_config_idle_shutdown_update_shutdown_timeout = f"""
    The time interval in minutes.
    Valid values: {IDLE_SHUTDOWN_TIME.list()}
    """

    # database-config: idle-shutdown delete command
    database_config_idle_shutdown_delete = """
    Delete the idle-shutdown configuration for a particular database.
    """
    database_config_idle_shutdown_delete_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    database_config_idle_shutdown_delete_shutdown_permanent = f"""
    If delete the idle shutdown job permanently.
    Default to False.
    """

    # database-config: auto-scale command
    database_config_auto_scale = """
    The database configuration for auto-scaling.
    """

    # database-config: auto-scale list command
    database_config_auto_scale_list = """
    List the auto-scaling configuration for a particular database.
    """
    database_config_auto_scale_list_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    database_config_auto_scale_list_enabled = """
    Filter result by the enable flag. All schedule configures will be returned if no flag is specified.
    """

    # database-config: auto-scale update command
    database_config_auto_scale_update = """
    Update the auto-scaling configuration for a particular database.
    """
    database_config_auto_scale_update_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    database_config_auto_scale_update_client_drain_time = f"""
    The subclusters session numbers will be monitored periodically based on this selected time interval.
    Default to 5.
    """
    database_config_auto_scale_update_sequence_count = """
    The subcluster session numbers will be checked against threshold after checked this number of rounds.
    A secondary subcluster will be started/stopped when total running sessions remain increased/decreased
    for the duration of the specified period.
    Default to 5.
    """
    database_config_auto_scale_update_max_sessions = """
    The maximum session numbers to trigger auto scale.
    Default to 5.
    """

    # database-config: auto-scale delete command
    database_config_auto_scale_delete = """
    Delete the auto-scaling configuration for a particular database.
    """
    database_config_auto_scale_delete_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    database_config_auto_scale_shutdown_permanent = f"""
    If delete the auto-scaling job permanently.
    Default to False.
    """

    ########################
    ## Subcluster Service ##
    ########################
    subcluster_header = """
    Manage subclusters.
    """

    # subcluster: start command
    subcluster_start = """
    Start the subcluster.
    """
    sub_start_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    sub_start_module = f"""
    The subcluster_id of the subcluster to be started.
    Valid values: {VAAS_MODULES.subcluster_list()}
    """

    # subcluster: stop command
    subcluster_stop = """
    Stop the subcluster.
    """
    sub_stop_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    sub_stop_module = f"""
    The subcluster_id of the subcluster to be stopped.
    Valid values: {VAAS_MODULES.subcluster_list()}
    """

    # subcluster: create command
    subcluster_create = """
    Create a new subcluster.
    """
    sub_create_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    sub_create_instance_type = f"""
    The instance type for the subcluster.
    Valid values: {AWS_INSTANCE_TYPES.list()}
    """
    sub_create_nodes = f"""
    The node count for the subcluster.
    Valid values: {VALID_NODES_NUMBERS.list()}
    """
    sub_create_module = f"""
    The subcluster_id of the subcluster to be created.
    Valid values: {VAAS_MODULES.subcluster_list()}
    """
    sub_create_subcluster_name = f"""
    The name of the subcluster.
    {SUBCLUSTER_NAME_NOTE}
    """

    # subcluster: drop command
    subcluster_drop = """
    Drop an existing subcluster.
    """
    sub_drop_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    sub_drop_module = f"""
    The subcluster_id of the subcluster to be dropped.
    Valid values: {VAAS_MODULES.subcluster_list()}
    """

    ####################
    ## Backup Service ##
    ####################
    backup_header = """
    Backup and restore the database.
    """

    # backup: list command
    backup_list = """
    Get a list of backup of all vbr configuration files ( *.ini ) 
    located in the the /opt/vertica/config directory.
    """
    backup_list_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """

    # backup: create command
    backup_create = """
    Create a backup archive based on the ini file.
    """
    backup_create_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    backup_create_config_script_base = """
    The vbr configuration file name located under /opt/vertica/config directory.
    """

    # backup: restore command
    backup_restore = """
    Restore a backup from a backup archival ID.
    """
    backup_restore_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    backup_restore_archive_id = """
    The generated timestamp after creating a backup. For example: 20211103_020007
    """
    backup_restore_include_objects = """
    The database objects or patterns of objects to restore from a full or object-level backup. 
    Use commas to delimit multiple objects and wildcard patterns.
    For example: 'table_one, table_two' for specific objects or '*' for all the tables.
    """

    #####################
    ## Session Service ##
    #####################
    session_header = """
    Manage sessions.
    """

    # session: list command
    session_list = """
    Get a list of sessions from certain database.
    """
    session_list_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """

    # session: remove command
    session_remove = """
    Delete a session with a specific seesion id.
    """
    session_remove_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    session_remove_id = """
    The active session ID on running nodes.
    """

    ##################
    ## Task Service ##
    ##################
    task_header = """
    Manage tasks.
    """

    # task: list command
    task_list = """
    Get a list of tasks.
    """
    task_list_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    task_list_type = f"""
    The task type to filter.
    Valid values: {VALID_TASK.list()}
    """

    # task: get command
    task_get = """
    Get the particular task details.
    """
    task_get_id = """
    The task ID associated with a specific job. For example: e48e02af-459a-4d17-a15b-e3b4f0d0a978
    """

    # task: status command
    task_status = """
    Get the latest task details.
    """

    ##################
    ## Cron Service ##
    ##################
    cron_header = """
    Manage the scheduler.
    """

    # cron: list command
    cron_list = """
    Get a list of cron job associated with the database.
    """
    list_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """

    # cron: add command
    cron_add = """
    Create a scheduled start/stop cron job.
    """
    add_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    add_module = f"""
    The subcluster_id for adding the cron job.
    Valid values: {VAAS_MODULES.list()}
    """
    add_cron_name = f"""
    The name of the cron job.
    {CRON_NAME_NOTE}
    """
    add_cron_action = f"""
    The cron action for the cron job to start/stop the instances.
    Valid values: {CRON_ACTION.list()}
    """
    add_cron_expression = """
    The schedule cron expression for the nodes.
    Use cron expression such as "59 02 * * ? *".
    """

    # cron: remove command
    cron_remove = """
    Delete a scheduled start/stop cron job.
    """
    remove_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    remove_module = f"""
    The subcluster_id for removing the cron job.
    Valid values: {VAAS_MODULES.list()}
    """
    remove_cron_name = f"""
    The name of the cron job.
    {CRON_NAME_NOTE}
    """
    remove_cron_action = f"""
    The cron action for the cron job to start/stop the instances.
    Valid values: {CRON_ACTION.list()}
    """

    # cron: set command
    cron_set = """
    Enable or Disable a cron job from the database.
    """
    set_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    set_module = f"""
    The subcluster_id for toggling the cron job.
    Valid values: {VAAS_MODULES.list()}
    """
    set_cron_name = f"""
    The name of the cron job.
    {CRON_NAME_NOTE}
    """
    set_cron_action = f"""
    The cron action for the cron job to start/stop instances.
    Valid values: {CRON_ACTION.list()}
    """
    set_action = f"""
    The action for the cron job to enable/disable it.
    Valid values: {TOGGLE_ACTION.list()}
    """

    # cron: update command
    cron_update = """
    Update an existing cron job.
    """
    update_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    update_module = f"""
    The subcluster_id for updating the cron job.
    Valid values: {VAAS_MODULES.list()}
    """
    update_cron_name = f"""
    The name of the cron job.
    {CRON_NAME_NOTE}
    """
    update_cron_action = f"""
    The cron action for the cron job to start/stop the instances.
    Valid values: {CRON_ACTION.list()}
    """
    update_cron_expression = """
    The schedule cron expression for the nodes.
    Use cron expression such as "59 02 * * ? *".
    """

    ####################
    ## Report Service ##
    ####################
    report_header = """
    Show and generate reports.
    """

    # report: show command
    report_show = """
    Show a dc report.
    """
    report_show_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    report_show_module = f"""
    The subcluster_id for showing the report.
    Valid values: {VAAS_MODULES.list()}
    """
    report_show_report_name = f"""
    The name of the report to show.
    Valid values: {VALID_REPORT_NAME.list()}
    """
    report_show_range = f"""
    The time range of the report to show.
    Valid values: {VALID_REPORT_RANGE.list()}
    """

    # report: generate command
    report_generate = """
    Generate a dc report.
    """
    report_generate_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    report_generate_report_name = f"""
    The name of the report to generate.
    Valid values: {VALID_REPORT_NAME.generate_list()}
    """

    #################
    ## DNS Service ##
    #################
    dns_header = """
    Manage DNS.
    """

    # dns: list command
    dns_list = """
    List DNS records of the vertica clusters.
    """
    dns_list_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    dns_list_dnsname = f"""
    The dns name of the record.
    {DNS_NAME_NOTE}
    """

    # dns: create command
    dns_create = """
    Create DNS (A) record for the cluster(s).
    """
    dns_create_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    dns_create_module = f"""
    The subcluster_id for creating the DNS record.
    Valid values: {VAAS_MODULES.list()}
    """
    dns_create_dnsname = f"""
    The dns name of the record.
    {DNS_NAME_NOTE}
    """

    # dns: remove command
    dns_remove = """
    Delete a single DNS (A) record by name.
    """
    dns_remove_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    dns_remove_dnsname = f"""
    The dns name of the record.
    {DNS_NAME_NOTE}
    """

    # dns: update command
    dns_update = """
    Update DNS (A) record for the cluster(s).
    """
    dns_update_name = f"""
    The name of the database.
    {DB_NAME_NOTE}
    """
    dns_update_module = f"""
    The subcluster_id for updating the DNS record.
    Valid values: {VAAS_MODULES.list()}
    """
    dns_update_dnsname = f"""
    The dns name of the record.
    {DNS_NAME_NOTE}
    """
