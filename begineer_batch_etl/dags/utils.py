from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.exceptions import AirflowFailException


def check_bucket_paths_exists(bucket_name: str, paths: list[str]) -> bool:
    """
    Checks if paths in a list exist on an S3 Bucket

    Arguments:
        bucket_name: str
            Bucket to scan
        paths: list[str]
            Paths to check for
    """
    s3_hook = S3Hook("AWS_CONN")

    prefixes_not_found:list[bool] = [
        path
        for path in paths
        if not s3_hook.check_for_prefix(
            prefix=path,
            delimiter="/",
            bucket_name=bucket_name
        )
    ]

    if len(prefixes_not_found) >= 1:
        raise AirflowFailException(f"Directory {prefixes_not_found} not found in bucket:{bucket_name}")
    else:
        True

def upload_to_s3(file_path: str, save_as: str, bucket_name: str) -> None:
    """
    Push file from local disk to S3 bucket.

    Arguments:
    ---------
    filename: str
            File to be sent.
    bucket_name: str
            bucket name to send file to.
    """
    s3_hook = S3Hook("s3_conn")
    s3_hook.load_file(
        filename=file_path, key=save_as, bucket_name=bucket_name, replace=True
    )
    # Print log msg reporting about the success here
