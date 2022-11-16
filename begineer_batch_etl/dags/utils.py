from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.exceptions import AirflowFailException

def check_bucket_path_exists(bucket_name: str, path: str) -> bool:
    s3_hook = S3Hook("AWS_CONN")
    prefix_exists = s3_hook.check_for_prefix(
        prefix=path,
        delimiter="/",
        bucket_name=bucket_name
    )
    print(f"Prefix Exists: {prefix_exists}")
    if not prefix_exists:
        raise AirflowFailException(f"Directory {path} not found in bucket:{bucket_name}")

