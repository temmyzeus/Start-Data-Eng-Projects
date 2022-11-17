wget -P /data https://start-data-engg.s3.amazonaws.com/data.zip \
&& unzip /data/data.zip -x '__MACOSX/*' -N \
&& chmod 755 /data