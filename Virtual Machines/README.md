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

1. Start the machine in NAT mode and update
```bash
sudo apt-get update
```

2. Install MariaDB server and client
```bash
sudo apt install mariadb-server mariadb-client -y
```

3. Check the status, and then stop and disable MariaDB so it does not run on startup.
```bash
sudo systemctl status mariadb
sudo systemctl stop mariadb
sudo systemctl disable mariadb
```

4. Run mysql_secure_installation script to perform basic configuration of the database.
```bash
sudo mysql_secure_installation
```

5. Shutdown the machines and switch to custom host-only adapter.
```bash
sudo shutdown -h now
```

6. Start the machines in host-only mode and edit the hosts file to include the IPs of each VM.
```bash
sudo nano /etc/hosts

# Set the IPs and hostnames of each VM. 
127.0.0.1 localhost
#127.0.1.1 uone

192.168.56.8     hostnameone
192.168.56.9     hostnametwo
192.168.56.10    hostnamethree
```

7. Configure the MariaDB cluster.
```bash
# Ensure that the database is stopped on each VM
sudo systemctl stop mariadb

# Update
sudo updatedb

# Edit the 60-galera.cnf file
cd /etc/mysql/mariadb.conf.d/
sudo nano 60-galera.cnf
```

8. Configure the 60-galera.cnf file with the following settings:
```bash
[galera]
# Mandatory settings
wsrep_on        = ON
wsrep_provider=/usr/lib/galera/libgalera_smm.so
wsrep_cluster_name    = "clustername"
# Enter the IP address for each VM: 
wsrep_cluster_address    = gcomm://192.168.56.8,192.168.56.9,192.168.56.10
binlog_format    = row
default_storage_engine    = InnoDB
innodb_autoinc_lock_mode    = 2

# Allow server to accept connections on all interfaces.
bind-address = 0.0.0.0

# Optional settings
wsrep_slave_threads = 1
innodb_flush_log_at_trx_commit = 0

# Node Configuration: Set to this VMs IP
wsrep_node_address = "192.168.56.8"
wsrep_node_name = "this_nodes_hostname"
```

9. Edit the 50-server.cnf file
    Set the bind address to the IP of the associated VM/server
```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf 

# Set the bind address in the file:
bind-address    = 192.168.56.8
```

10. Starting the MariaDB cluster
```bash
# Always run this on the primary VM first to initiate the cluster: 
sudo galera_new_cluster

# Then run this on the other VMs to start the server: 
sudo systemctl start mariadb

# After executing those commands, check the cluster size. It should be 3.
sudo mysql -u root -p -e "SHOW STATUS LIKE 'wsrep_cluster_size';"
```

11. Access the MariaDB command line interface (CLI)
```bash
sudo mysql -u root -p
```

12. Commands you can use here:
    Execute any MariaDB SQL syntax to create tables and insert values. 
```bash
create database <name>;     # Create a new database
show databases;    # Show a list of available databases
use <database>;    # Access a database
show tables;    # Show tables within a database. 

# Create a new user and grant privileges
CREATE USER 'username'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'username'@'%' IDENTIFIED BY 'password';

# Grant privileges to a specific IP to connect to the database via an IDE
GRANT ALL PRIVILEGES ON *.* TO 'username'@'<IP>' IDENTIFIED BY 'password';
```
 
14. Stopping the MariaDB cluster
    Always stop the other VMs before the primary one. 
```bash
sudo systemctl stop mariadb
```


