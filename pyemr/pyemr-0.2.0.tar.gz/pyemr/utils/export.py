"""A collection of aws tools"""
from pyemr.utils.config import get_package_dir,get_project_attrs,get_emails,get_project_attr,get_config_attr,get_emails,get_cluster_name
from pyemr.utils.emr import get_cluster_id
from pyemr.utils.build import get_spark_step
from black import format_str, FileMode
from jinja2 import Template

AIRFLOW_TEMPLATE_PATH = 'files/templates/airflow_spark_step.template.py'

def export_airflow_template(
        local_script_path,
        submit_mode='client',
        action_on_failure='CONTINUE',
        *args,
        **kwargs,
    ):
    
    package_dir = get_package_dir()
    with open(f'{package_dir}/{AIRFLOW_TEMPLATE_PATH}') as file:
        airflow_template = file.read()
    
    param = get_project_attrs(['name', 'version','description'])
    param['emails'] = get_emails()
    param['owner'] = get_project_attr('authors')[0]
    param['emr_cluster_name'] = get_cluster_name()
    param['emr_cluster_id'] = get_cluster_id()
    param['stage'] = get_config_attr('stage')
    param['spark_step'] = get_spark_step(
        local_script_path,
        submit_mode,
        action_on_failure,
        *args,
        **kwargs,
    )
    
    param['hadoop_jar_args'] = param['spark_step']['HadoopJarStep'].pop("Args")
    param['schedule_interval'] =''
    param['spep_id_formula'] = "{{ task_instance.xcom_pull(task_ids='add_steps', key='return_value')[0] }}"
    
    airflow_template = Template(airflow_template)
    airflow_script = airflow_template.render(**param)
    airflow_script = format_str(airflow_script, mode=FileMode())
    
    with open('./airflow_dag.py', 'w') as file:
        file.write(airflow_script)
