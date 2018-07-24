deploy_loop_counter=0
deploy_loop_counter_max=1
propose_loop_counter=0
propose_loop_counter_max=10
grpc_host="52.119.8.92"
contract_amount=10

while [[ ${propose_loop_counter} -lt ${propose_loop_counter_max} ]]; do
    deploy_loop_counter=0
    while [[ ${deploy_loop_counter} -lt ${deploy_loop_counter_max} ]]; do
        echo $deploy_loop_count
        for i in `ls /usr/share/rnode/examples/hello_world_again.rho`; do
            echo "running deploy with ${i}";
            rnode --grpc-host ${grpc_host} deploy ${i} &
        done
        deploy_loop_counter=$((${deploy_loop_counter}+1))
    done
    echo "done"
    rnode --grpc-host ${grpc_host} propose
    propose_loop_counter=$((${propose_loop_counter}+1))
    echo "start new propose loop"
done
