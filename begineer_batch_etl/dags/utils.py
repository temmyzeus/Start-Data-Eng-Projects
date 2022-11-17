from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.exceptions import AirflowFailException

def apply_false_mask(values:list, mask:list[bool]):
    """
    Get the subset elements or all elements of a list by \ 
    selecting positions based on list of boolean of same length. \
    The boolean returns the value when `False`.

    :param values: List to be subsetted
    :type values:list
    :param mask: Lis of booleans (masks) by which to map to each position
    :type mask:list[bool]
    """
    if len(values) != len(mask):
        # Wrong Error Exception
        raise AttributeError()

    # Guard clause to check if mask contains boolean
    if not all([isinstance(_, bool) for _ in mask]):
        # Wrong Error Exception
        raise AttributeError()

    for value, bool_val in zip(values, mask):
        if not bool_val:
            yield value

def check_bucket_paths_exists(bucket_name: str, paths: list[str]) -> bool:
    """
    Add Docstring
    """
    s3_hook = S3Hook("AWS_CONN")

    prefix_existence:list[bool] = []
    for path in paths:
    prefix_exists = s3_hook.check_for_prefix(
        prefix=path,
        delimiter="/",
        bucket_name=bucket_name
    )
        print(f"{path} Prefix Exists: {prefix_exists}")
        prefix_existence.append(prefix_exists)
    
    if not all(prefix_existence):
        # Write a functionaloty to find the positions tahta re False in `all_prefix_exists` and based on that
        # check paths topath that does not exists so you can put it into the Exception message
        paths_not_found = list(apply_false_mask(paths, prefix_existence))
        raise AirflowFailException(f"Directory {paths_not_found} not found in bucket:{bucket_name}")


