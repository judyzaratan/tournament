# Tournament

## Description
This project keeps track of players and matches for a Swiss pairing tournament.
A PostgreSQL database is used to record players, match pairings, and wins/losses.
This application is written in Python.  [Vagrant](https://www.vagrantup.com/) is used to create a virtual environment to run and test the application.  To see what is installed in the virtual machine, refer to pg_config.sh file.

##How to run application

1) Run a virtual machine
⋅⋅⋅Vagrantfile is included in repository.  Please run following commands in Terminal:

```
vagrant up
vagrant ssh
```

2) When virtual machine is up and running, change directory containing files
```
cd /vagrant/tournament
```

3) Create database and import database schemas, by typing in Terminal:
```
psql -f tournament.sql
```

3) Run test suite file to verify functions are functioning as they should be.
```
python tournament_test.py
```
