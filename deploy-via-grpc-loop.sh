#!/usr/bin/env bash
# apt update && apt -y install wget nano && wget https://repo.pyr8.io/rchain/downloads/dev/rnode_0.5.3_all.deb && apt -y install ./rnode_0.5.3_all.deb
sudo docker run -dit --name deploy.rchain.coop --network rchain.coop debian
deploy_loop_counter=0
deploy_loop_counter_max=1
propose_loop_counter=0
propose_loop_counter_max=10
grpc_hosts="peer0.rchain.coop peer1.rchain.coop peer2.rchain.coop peer3.rchain.coop peer4.rchain.coop"
contract_amount=10

function grpc_deploy_from_host {
    if [[ ! $1 ]]; then
	echo "Missing param grpc_host"
        exit
    fi
    local grpc_host="$1"

    echo "Running deploy/propose on ${grpc_host}"
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
}

for grpc_host in ${grpc_hosts}; do
    grpc_deploy_from_host ${grpc_host} &
done
