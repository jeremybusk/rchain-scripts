#!/usr/bin/env python3.7
from nacl.public import PrivateKey, PublicKey
import nacl.encoding
import nacl.signing
import random
import sys
from pprint import pprint
import shutil
import os
import subprocess
import time
import argparse

peers_total = 5
bonds_file = "/tmp/bonds.txt"
tmp_dir = "/tmp/rchain.coop"

parser = argparse.ArgumentParser(
             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-b", "--boot",
                    action='store_true',
                    help="boot network by creating resources and starting services by network name")
parser.add_argument("-l", "--list",
                    action='store_true',
                    help="list all peers values")
parser.add_argument("-a", "--amount",
                    dest='amount',
                    type=int,
                    default="3",
                    help="amount of peer instances, including bootstrap, to start")
args = parser.parse_args()

# Print -h/help if no args
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)


def display_peer_instances_values():
    for i in Peer.instances:
        print(i)
        pprint(vars(i))

def stop_all_peers():
    # Stop all previous instances
    subprocess.run(["pkill", "java"])
    time.sleep(5)

def add_entropy_to_host():
    #sysctl kernel.random.entropy_avail
    subprocess.run(["rngd", "-r", "/dev/urandom"])
    #sysctl kernel.random.entropy_avail
        

def main():
    # if args.list:
    #     print("yes")
    #     display_peer_instances_values()
    #     return
    # sys.exit()
    stop_all_peers()
    # a = Peer()
    # a.set_validator_keys() 
    # a.set_cmd()
    # a.start()
    # time.sleep(5)
    # b = Peer()
    # b.set_validator_keys() 
    # b.set_cmd()
    # b.start()
    # return
    #instancelist = [ MyClass() for i in range(29)]
    peer = {} 
    #create_bonds_file()
    for i in range(args.amount+1):
        add_entropy_to_host()
        print(i)
        peer[i] = Peer()
        print(peer[i].name)
        peer[i].set_validator_keys()
        peer[i].set_cmd()
        peer[i].start()
        time.sleep(10)

    display_peer_instances_values()

#     return
# 
#     a = Peer()
#     a.set_validator_keys() 
#     a.set_cmd()
#     a.start()
#     b = Peer()
#     b.set_validator_keys() 
#     b.set_cmd()
#     b.start()
#     return
#     # print(a.validator_private_key)
#     # print(a.validator_public_key)
#     # print(a.bonds_file_line)
#     for i in Peer.instances:
#         #print("instance 1")
#         #print(i.name)
#         print(i)
#         pprint(vars(i))
#     a.start()
#     return
#     print(a.cmd)
#     print(a)
#     print(a.count)
#     b = Peer()
#     b.set_cmd()
#     print(b.count)
#     print(b.cmd)
#     print(a.count)
#     print(a.name)
#     print(b.name)
# 
#     # for peer_num in range(peers_total):
#     #     print(peer_num)
#     #     if peer_num == 0:
#     #         port = port_start_num+peer_num
#     #         metrics_port = port+1
#     #         grpc_port = metrics_port+1
#     #         http_port = grpc_port+1
#     #         print("Starting bootstrap peer in standalone mode.")
#     #         cmd = f"rnode --port {port} --metrics-port {metrics_port} --grpc-port {grpc_port} --http-port {http_port} --validator-private-key"
#     #         print(cmd)
#     #         peer_num += 1
# 
#     #     else:
#     #         print("Starting peer using bootstrap server.")
#     # #--port --metrics-port --grpc-port --http-port --validator-private-key



def get_private_validator_key(): 
    pass


def create_empty_bonds_file():
    # Create or zero out bonds file so it is empty and can be mounted as volumes by containers 
    try:
        with open(bonds_file, 'w+') as f:
            f.write("")
    except IOError as e:
        print(f"Failed to open or write to file {e}.")



def create_bonds_file(): 
    create_empty_bonds_file()

    print(f"Populating bonds file {bonds_file}")
    bond_weight = random.randint(1,100)
    #line = f"{encoded_public_key} {bond_weight}".decode('utf-8')
    line = str(f"{encoded_public_key} {bond_weight}")
    print(line)
    try:
        with open(bonds_file, 'a+') as f:
            f.write(f"{line}\n")
    except IOError as e:
        print(f"Failed to open or write to file {e}.") 


class Peer:
    count = 0
    instances = []
    next_available_port = 10000


    # Remove app temp directory if it exits and recreate 
    #tmp_dir = os.path.join('dataset3', 'dataset')
    if os.path.exists(tmp_dir) and os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    # Create empty bonds files
    try:
        with open(bonds_file, 'w+') as f:
            f.write("")
    except IOError as e:
        print(f"Failed to open or write to file {e}.")


    def __init__(self):
        name = f"peer{Peer.count}.rchain.coop"
        #self.name = f"peer{Peer.count}.rchain.coop"
        self.name = name 
        #self.cmd = self.get_cmd(self) 
        #port_start_num = 10000


        # Create peer data directory.
        data_dir = f"{tmp_dir}/{name}"
        self.log_file = f"{data_dir}/rnode.log" 
        self.data_dir = data_dir 
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        Peer.instances.append(self)
        self.number = Peer.count 
        Peer.count += 1

    def set_validator_keys(self):
        #for i in range(peers_total):
        # pynacl for libsodium
        # import nacl # libsodium/ed25519 support
        self.private_key = PrivateKey.generate()
        encoded_private_key = self.private_key.encode(encoder=nacl.encoding.Base16Encoder).decode('utf-8').lower()
        encoded_public_key = self.private_key.public_key.encode(encoder=nacl.encoding.Base16Encoder).decode('utf-8').lower()
        signing_key = nacl.signing.SigningKey.generate() 
        verify_key = signing_key.verify_key
        self.validator_private_key = signing_key.encode(encoder=nacl.encoding.Base16Encoder).lower().decode('utf-8')
        self.validator_public_key = verify_key.encode(encoder=nacl.encoding.Base16Encoder).lower().decode('utf-8')
        print(self.validator_private_key)

        self.bond_weight = random.randint(1,100)
        self.bonds_file_line = f"{self.validator_public_key} {self.bond_weight}"
        
        try:
            with open(bonds_file, 'a+') as f:
                f.write(f"{self.bonds_file_line}\n")
        except IOError as e:
            print(f"Failed to open or write to file {e}.") 
    
        #print(f"Populating bonds file {bonds_file}")
        #line = f"{encoded_public_key} {bond_weight}".decode('utf-8')
        #line = str(f"{encoded_public_key} {bond_weight}")
        #line = bonds_file_line 
        #print(line)

        # #bonds_private_public_key_array = [encoded_private_key]

        # #return encoded_private_key, encoded_public_key
        # self.encoded_private_key
        # encoded_public_key


    def start(self):
        #r = subprocess.run(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.p = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.output = self.p.stdout.read()
        print(self.cmd)
        print(self.output)
        for line in self.output.splitlines():
            print(line.decode('utf-8'))
            # if args.network in line.decode('utf-8'):
            # if "alsdjfalskdjf" in line.decode('utf-8'):
            #     print(line.decode('utf-8'))
   
 
    def stop(self):
        self.p.terminate()
        # #r = subprocess.run(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # r = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # for line in r.stdout.splitlines():
        #     #if args.network in line.decode('utf-8'):
        #     if "alsdjfalskdjf" in line.decode('utf-8'):
        #         print(line.decode('utf-8'))


    def set_cmd(self):
        self.port = Peer.next_available_port 
        Peer.next_available_port += 1
        self.grpc_port = Peer.next_available_port 
        Peer.next_available_port += 1
        self.metrics_port = Peer.next_available_port 
        Peer.next_available_port += 1
        self.http_port = Peer.next_available_port 
        Peer.next_available_port += 1
        print(self.number) #sadlfkjasldfjalsjfd
        if self.number == 0:
            #bootstrap_node_demo_key=(
            self.node_key=(
                "-----BEGIN PRIVATE KEY-----\n"
                "MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgYcybGU15SCs2x+5I\n"
                "JHrzzBHZ0c7k2WwokG6yU754XKKgCgYIKoZIzj0DAQehRANCAAR/MkqpcKUE+NtM\n"
                "d8q7/IPih2vO6oMjm2ltSA2nSrueNd+jpLvxDQpRYScJBDyeylfB1VkPdpw9oqFQ\n"
                "Y5huc38x\n"
                "-----END PRIVATE KEY-----\n"
            )
            #bootstrap_node_demo_cert=(
            self.node_cert=(
                "-----BEGIN CERTIFICATE-----\n"
                "MIIBXzCCAQKgAwIBAgIIU0qinJbBW5MwDAYIKoZIzj0EAwIFADAzMTEwLwYDVQQD\n"
                "EyhjYjc0YmEwNDA4NTU3NGU5ZjAxMDJjYzEzZDM5ZjBjNzIyMTljNWJiMB4XDTE4\n"
                "MDYxMjEzMzEyM1oXDTE5MDYxMjEzMzEyM1owMzExMC8GA1UEAxMoY2I3NGJhMDQw\n"
                "ODU1NzRlOWYwMTAyY2MxM2QzOWYwYzcyMjE5YzViYjBZMBMGByqGSM49AgEGCCqG\n"
                "SM49AwEHA0IABH8ySqlwpQT420x3yrv8g+KHa87qgyObaW1IDadKu54136Oku/EN\n"
                "ClFhJwkEPJ7KV8HVWQ92nD2ioVBjmG5zfzEwDAYIKoZIzj0EAwIFAANJADBGAiEA\n"
                "62Po1SVQyJB/2UeG5B9O1oTTlhYrLvLTWH24YiH4U4kCIQDrPa3Qop3yq83Egdq0\n"
                "VkEqI2rycmgp03DXsStJ7IGdBQ==\n"
                "-----END CERTIFICATE-----\n"
            )
            
            #self.node_key_file = '/tmp/node.key.pem'
            #self.node_cert_file = '/tmp/node.certificate.pem'
            self.node_key_file = f'{self.data_dir}/node.key.pem'
            self.node_cert_file = f'{self.data_dir}/node.certificate.pem'
            with open(self.node_key_file, 'w') as f:
                f.write(self.node_key)
            with open(self.node_cert_file, 'w') as f:
                f.write(self.node_cert)
            print("Starting bootstrap peer in standalone mode.")
            self.cmd = f"rnode --grpc-port {self.grpc_port} run --standalone --port {self.port} --metrics-port {self.metrics_port} --http-port {self.http_port} --key {self.node_key_file} --validator-private-key {self.validator_private_key} --validator-public-key {self.validator_public_key} --bonds-file {bonds_file} --data_dir {self.data_dir} > {self.log_file} 2>&1 &"
            #print(cmd)
            #return cmd
            #peer_num += 1
        else:
            print("Starting peer using bootstrap server.")
            #self.cmd = f"rnode --grpc-port {self.grpc_port} run --port {self.port} --metrics-port {self.metrics_port} --http-port {self.http_port} --validator-private-key {self.validator_private_key} --validator-public-key {self.validator_public_key}"
            #self.cmd = f"rnode --grpc-port {self.grpc_port} run --port {self.port} --metrics-port {self.metrics_port} --http-port {self.http_port} --validator-private-key {self.validator_private_key} --validator-public-key {self.validator_public_key}"
            #self.cmd = f"rnode --grpc-port {self.grpc_port} run --port {self.port} --metrics-port {self.metrics_port} --http-port {self.http_port} --validator-private-key {self.validator_private_key} --validator-public-key {self.validator_public_key} --data_dir {self.data_dir} --bootstrap rnode://cb74ba04085574e9f0102cc13d39f0c72219c5bb@52.119.8.99:10000 > {self.log_file} 2>&1 &"
            self.cmd = f"rnode --grpc-port {self.grpc_port} run --port {self.port} --metrics-port {self.metrics_port} --http-port {self.http_port} --validator-private-key {self.validator_private_key} --validator-public-key {self.validator_public_key} --data_dir {self.data_dir} --bootstrap rnode://cb74ba04085574e9f0102cc13d39f0c72219c5bb@127.0.0.1:10000 > {self.log_file} 2>&1 &"
            #self.cmd = f"rnode --grpc-port {self.grpc_port} run --port {self.port} --metrics-port {self.metrics_port} --http-port {self.http_port} --validator-private-key poo --validator-public-key pee --data_dir {self.data_dir} "
        #return cmd


    def display_count(self):
        print (count)
 
    def display_peer_attributes(self):
        pass


if __name__ == "__main__":
    main()


