docker run -e BOOTSTRAP_SERVER=$1 -e TOPIC=$2 -p 8080:8080 --network=host hendrikreiter/def-loadtest-backend:0.1.0