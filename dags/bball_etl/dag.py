"""
Example DAG demonstrating the usage of the TaskFlow API to execute Python functions natively and within a
virtual environment.
"""
from __future__ import annotations

import logging
import shutil
import sys
import tempfile
import time
from pprint import pprint

import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import ExternalPythonOperator, PythonVirtualenvOperator

log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable

BASE_DIR = tempfile.gettempdir()

def x():
    pass

with DAG(
    dag_id="baseball-etl",
    schedule=None, # "0 * * * 1"
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["baseball","etl"],
    # owner="trevor_jordan"
) as dag:

    # [START howto_operator_python]
    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs)
        print(ds)
        return "Whatever you return gets printed in the logs"

    run_this = print_context()
    # [END howto_operator_python]

    # [START howto_operator_python_render_sql]
    @task(task_id="log_sql_query", templates_dict={"query": "sql/sample.sql"}, templates_exts=[".sql"])
    def log_sql(**kwargs):
        logging.info("Python task decorator query: %s", str(kwargs["templates_dict"]["query"]))

    log_the_sql = log_sql()
    # [END howto_operator_python_render_sql]

    # [START howto_operator_python_kwargs]
    # Generate 5 sleeping tasks, sleeping from 0.0 to 0.4 seconds respectively
    for i in range(5):

        @task(task_id=f"sleep_for_{i}")
        def my_sleeping_function(random_base):
            """This is a function that will run within the DAG execution"""
            time.sleep(random_base)

        sleeping_task = my_sleeping_function(random_base=float(i) / 10)

        run_this >> log_the_sql >> sleeping_task
    # [END howto_operator_python_kwargs]

    if not shutil.which("virtualenv"):
        log.warning("The virtalenv_python example task requires virtualenv, please install it.")
    else:
        # [START howto_operator_python_venv]
        @task.virtualenv(
            task_id="virtualenv_python", requirements=["colorama==0.4.0"], system_site_packages=False
        )
        def callable_virtualenv():
            """
            Example function that will be performed in a virtual environment.

            Importing at the module level ensures that it will not attempt to import the
            library before it is installed.
            """
            from time import sleep

            from colorama import Back, Fore, Style

            print(Fore.RED + "some red text")
            print(Back.GREEN + "and with a green background")
            print(Style.DIM + "and in dim text")
            print(Style.RESET_ALL)
            for _ in range(4):
                print(Style.DIM + "Please wait...", flush=True)
                sleep(1)
            print("Finished")

        virtualenv_task = callable_virtualenv()
        # [END howto_operator_python_venv]

        sleeping_task >> virtualenv_task

        # [START howto_operator_external_python]
        @task.external_python(task_id="external_python", python=PATH_TO_PYTHON_BINARY)
        def callable_external_python():
            """
            Example function that will be performed in a virtual environment.

            Importing at the module level ensures that it will not attempt to import the
            library before it is installed.
            """
            import sys
            from time import sleep

            print(f"Running task via {sys.executable}")
            print("Sleeping")
            for _ in range(4):
                print("Please wait...", flush=True)
                sleep(1)
            print("Finished")

        init = callable_external_python()
        bbref = callable_external_python()
        retro = callable_external_python()
        lahman = callable_external_python()
        # [END howto_operator_external_python]

        # [START howto_operator_external_python_classic]
        transform = ExternalPythonOperator(
            task_id="external_python_classic",
            python=PATH_TO_PYTHON_BINARY,
            python_callable=x,
        )
        # [END howto_operator_external_python_classic]

        # [START howto_operator_python_venv_classic]
        load = PythonVirtualenvOperator(
            task_id="virtualenv_classic",
            requirements="colorama==0.4.0",
            python_callable=x,
        )
        # [END howto_operator_python_venv_classic]

        init >> [bbref,retro,lahman] >> transform >> load