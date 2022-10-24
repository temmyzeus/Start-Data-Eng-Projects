echo -e "AIRFLOW_UID=$(id -u)" > begineer_batch_etl/.env
echo -e "AIRFLOW_GID=${id -g}" >> begineer_batch_etl/.env
echo "UID and GIU saved to .env file"