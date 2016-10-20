#!/bin/bash

echo "Space Guars executor"

echo -n "Run Server or Client [s/c]? "
read answer
if [ "$answer" == "s" ]; then
	cd Servidor/
	python servidor.py
elif [ "$answer" == "c" ]; then
	cd Cliente/
	echo -n "Dummy Bot: "
	read dummy
	echo -n "Smart Bot: "
	read smart
	echo -n "Server IP: "
	read ip
	echo -n "Server Port: "
	read port
	until [ "$dummy" = "0" ]; do
		echo "Dummy bot n: " $dummy
		printf "$ip\n$port\n" | python cliente_dummy.py > o.out &
		let "dummy -= 1"
	done
	until [ "$smart" = "0" ]; do
		echo "Smart bot n: " $smart
		printf "$ip\n$port\n" | python cliente_alumnos.py > o.out &
		let "smart -= 1"
	done
	exit 0
else
	clear
fi