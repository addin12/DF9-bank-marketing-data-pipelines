#!/bin/bash
fileid="1Fab7jePW3LKFUNyJf2BoH6ywrDiXatNt"
filename="bank_marketing.csv"
html=`curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}"`
curl -Lb ./cookie "https://drive.google.com/uc?export=download&`echo ${html}|grep -Po '(confirm=[a-zA-Z0-9\-_]+)'`&id=${fileid}" -o "/opt/airflow/${filename}"