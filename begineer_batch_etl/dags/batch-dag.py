from datetime import timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.s3 import S3CopyObjectOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago

from utils import check_bucket_path_exists

BUCKET_NAME:str = Variable.get("BUCKET_NAME")

default_args = {
	"email": [
		"awoyeletemiloluwa@gmail.com" #replace with airflow variable
	],
	"email_on_retry": False,
	"email_on_failure": False,
	"retry_delay": timedelta(seconds=30)
}

with DAG(
	"Batch-ETL-Pipeline",
	default_args=default_args,
	start_date=days_ago(1),
	schedule_interval=None,
	catchup=False
	) as dag:

	check_raw_stage_scripts = PythonOperator(
		task_id="check_raw_stage_script",
		python_callable=check_bucket_path_exists,
		op_kwargs={
			"bucket_name": BUCKET_NAME,
			"path": "raw"
		}
	)

	extract_user_purchase_data = PostgresOperator(
		task_id="extract_user_purchase_data",
		sql="./scripts/sql/extract_user_purchases.sql",
		postgres_conn_id="postgres_conn",
		database="postgres",
		params={
			"table_name": "user_purchases",
			"user_purchases_file": "/var/lib/postgresql/user_purchases.csv"
			}
	)
	
	# user_purchases_to_stage_data_lake = S3CopyObjectOperator(
	# 	task_id="user_purchases_to_stage_data_lake"
	# )

	[check_raw_stage_scripts, extract_user_purchase_data]
