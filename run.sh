#!/bin/bash
export FLASK_APP=flaskr
#export FLASK_ENV=development

flask init-db

if [ $# == 2 ]
then
    echo "以 $1 :$2 创建服务..."
    flask run -h $1 -p $2
else
    echo "以 默认选项 创建服务...(dafault:127.0.0.1:5000)"
    flask run
fi

