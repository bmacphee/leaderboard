#!/bin/bash
rm -rf package function.zip
pip install -r requirements.txt --target ./package
find ./package -name "*.dist-info" | xargs rm -rf
rm -rf package/boto3 package/botocore
find package -name __pycache__ | xargs rm -rf
cp -R config main package
cp .serverless-wsgi serverless_wsgi.py wsgi_handler.py package
cd package && zip -r9 ../function.zip . && cd -
