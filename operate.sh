if [ $# != 1 ]; then
    echo "Usage: $0 start|stop"
    exit 1
fi

if [ $1 = "start" ]; then
    nohup python3 flask_web/run.py > out.file 2>1 &
elif [ $1 = "stop" ]; then
    kill -9 $(netstat -nlp | grep :8080 | awk '{print $7}' | awk -F"/" '{ print $1 }')
fi