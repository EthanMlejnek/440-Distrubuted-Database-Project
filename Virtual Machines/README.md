# MariaDB Cluster Implementation
A deliverable for this project was to successfully configure and deploy a Distributed Database Management System (DDBMS) for a global digital marketing agency with locations in the United States, Japan, and Argentina. 

Three headless Ubuntu Server virtual machines were deployed via Oracle VirtualBox: https://ubuntu.com/download/server

Each virtual machine was configured with the following settings: 
* Base Memory: ~4000 MB (4G) or more
* 2 or more processors
* 15GB or more pre-allocated storage
* Custom Host-Only NIC utilizing DHCP for inital IP assignment

# Implementation Steps
The following steps were followed to configure each virtual machine: 

1. Start each machine in NAT mode to download relevant software and do the following:
    - Run update
```bash
sudo apt-get update
```
- Install MariaDB server and client
```bash
sudo apt install mariadb-server mariadb-client -y
```
