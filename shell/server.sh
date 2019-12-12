#!/bin/bash

filepath="/root/OperaAudio/start.py"

start(){
    nohup python $filepath>/root/OperaAudio/log 2>&1 &
    echo 'OperaAudio Server Service Start OK'
}


stop(){
    ps -ef | grep 'python /root/OperaAudio/start.py' | grep -v grep | awk '{print $2}' | xargs kill -9
}


restart(){
    stop
    echo 'OperaAudio Server Service Stop OK'
    start
    echo 'OperaAudio Server Service Start OK'
}


case $1 in
    start)
    start
    ;;
    stop)
    stop
    ;;
    restart)
    restart
    ;;
    *)
    start
esac