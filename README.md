
# RevServer

[![Python](https://img.shields.io/badge/Python-%E2%89%A5%203.6-yellow.svg)](https://www.python.org/)


## Purpose
RevServer is a small Framework that can generate curl commands for reverse shells and can host files on a webserver

Main features are:
- Start a webserver that hosts files for both windows and linux,
  - Log the IP of the get request for further use
- Generate a curl command to get these files and auto execute them,
- Generate a curl command compiled in duckyscript,
- Start a reverse handler for 1 connection (i will probably change that later).

## Installation
RevServer was developed and tested on **kali linux**.
First clone the repo using:
```
git clone https://github.com/SnapBanane/RevServer
cd ./RevServer
```
Then install all requirements:
```
sudo ./setup.sh
```
This will take a bit if you not have **Terminator** installed.

## Usage
To start RevServer use:
```
sudo python3 RevServer.python
```
When RevServer is started you can use *help* to open a helpful menu of all the commands there are.
- Modify the linux.sh and windows.bat files to the code you want to execute when the curl commands is used.

## Example Usage

Start RevServer.
```
cd RevServer
sudo python3 RevServer.py
```
Start a webserver.
```
server start
(stop using "server stop")
```
Generate a curl command for linux compiled to ducky:
```
generate os=ubuntu ducky

for windows:

generate os=windows ducky
```
File will be generated in "Duckyscript.txt". We will assume that i put a reverse shell script in linux.sh so i need to start a listener. This script comes with a simple nc -lvnp [port] listener. To start it:
```
listen port=[port]

to stop the listener use:

listen stop
```
If you have any questions feel free to message me.
