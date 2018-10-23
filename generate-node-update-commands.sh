#!/usr/bin/env bash
# generate commands to update and run nodes in docker
timestamp=$(date "+%Y.%m.%d-%H.%M.%S")
docker_image="rchain/rnode:v0.7.1"
bootstrap_uri="rnode://8eb905149ee104ff8cd6f5f2197b1c78f23dc11c@52.119.8.200?protocol=40400&discovery=40404" 
deploy_timestamp="1540233008903"
required_sigs="15"
wallets_file="/var/lib/rnode/wallets.txt"
bonds_file="/var/lib/rnode/genesis/bonds.txt"
data_dir="/var/lib/rnode"
environment_vars="-e _JAVA_OPTIONS='-Xms20G -Xmx40G -XX:MaxMetaspaceSize=10G'"

count=0
for validator_private_key in $(cat /srv/rnode/public-keys.txt); do
    count=$((count+1))
    cmd="salt testnet${count}.pyr8.io cmd.run 'docker stop \$(docker ps -q); docker pull ${docker_image}; mkdir /bkp; cp -rp /var/lib/rnode /bkp/rnode.${timestamp}; rm -rf ${data_dir}/rspace; curl -s https://repo.pyr8.io/rchain/downloads/misc/testnetGenesisBonds.txt -o ${bonds_file}; curl -s https://repo.pyr8.io/rchain/downloads/misc/rhoc_rev_balances.txt -o ${wallets_file}; chown -R rnode:rnode ${data_dir}'"
    echo ${cmd}
    cmd="salt testnet${count}.pyr8.io cmd.run \"sudo docker run -u root ${environment_vars} --network host -v ${data_dir}:${data_dir} -dit ${docker_image} run -b '${bootstrap_uri}'  --deploy-timestamp ${deploy_timestamp} --required-sigs ${required_sigs} --data_dir ${data_dir} --wallets-file ${wallets_file} --bonds-file ${bonds_file} --map_size 17179869184 --genesis-validator --validator-private-key ${validator_private_key}\""
    echo ${cmd}
done
