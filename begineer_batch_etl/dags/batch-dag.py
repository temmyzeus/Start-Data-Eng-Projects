from datetime import timedelta

from airflow import DAG
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.providers.amazon.aws.operators.s3 import S3CopyObjectOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago

from utils import check_bucket_paths_exists

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
		python_callable=check_bucket_paths_exists,
		op_kwargs={
			"bucket_name": BUCKET_NAME,
			"paths": ["raw", "stage", "scripts"]
		}
	)

	extract_user_purchase_data = PostgresOperator(
		task_id="extract_user_purchase_data",
		sql="./scripts/sql/extract_user_purchases.sql",
		postgres_conn_id="RETAIL_DB_CONN",
		params={
			"table_name": "user_purchases",
			"user_purchases_file": "/data/database_dump/user_purchases.csv"
			}
	)

	user_purchase_to_stage_data_lake = LocalFilesystemToS3Operator(
		task_id="user_purchase_to_stage_data_lake",
		filename="/data/database_dump/user_purchases.csv",
		dest_key="raw/user_purchases.csv",
		dest_bucket=BUCKET_NAME,
		aws_conn_id="AWS_CONN",
		replace=False
	)

	user_purchase_stage_data_lake_to_redshift_table = RedshiftSQLOperator(
		task_id="user_purchase_stage_data_lake_to_redshift_table"
	)

	[check_raw_stage_scripts, extract_user_purchase_data] >> user_purchase_to_stage_data_lake
