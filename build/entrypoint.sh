#!/bin/bash
# Praetorian H2020 Project
# Work Package 6	:	Response Coordination
# Task 4			:	Integration with Social Media
# ~~~~~~~~~~~~~~~~~~~~
# Docker image entrypoint

# Grab the credentials
source /app/credentials.env

# Clone the code repo
git clone "https://${Github_Username}:${Github_Passcode}@github.com/UphillD/praetorian-backend"
cd praetorian-backend

# Customize text
ORANGE='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'		# No Color
bold=$(tput bold)
regular=$(tput sgr0)

# Set timezone
export TZ='Europe/Athens'

# Define function that displays help message
function help_msg () {
	echo -e 'Usage:'
	echo -e '\t docker run [OPTIONS] --name praetorian_backend --log-driver local --network host -t uphilld/praetorian:backend [ARGUMENT]'
	echo -e ''
	echo -e 'Options:'
	echo -e '\t -d      launches the container in background mode'
	echo -e '\t -it     launches the container in interactive mode'
	echo -e 'Arguments:'
	echo -e '\t(none)   launches both modules'
	echo -e '\t main    launches the main module (SMSTD & CO)'
	echo -e '\t aux     launches the aux module (PR)'
	echo -e '\t bash    launches an instance of bash'
	echo -e '\t help    prints this help message'
	echo -e ''
	echo -e 'Please note that the -it option is required if any argument is present.'
	echo -e 'If you just wish to launch everything normally in the background, run this:'
	echo -e '\t docker run -d --name praetorian_backend --log-driver local --network host -t uphilld/praetorian:backend'
	echo -e 'and if you wish to see the logs of the container, run this:'
	echo -e '\t docker logs praetorian_backend'
}

clear

# Launch all (no arguments)
if [ $# -eq 0 ]; then
	python3 -u main.py &
	python3 -u aux.py &
# Conditional launch (one argument)
elif [ $# -eq 1 ]; then
	case "$1" in
	"main")	python3 -u main.py ;;
	"aux")	python3 -u aux.py ;;
	"bash")	exec /bin/bash ;;
	"help") help_msg ;;
	*)		echo -e 'Non standard arguments detected.' && help_msg ;;
	esac
else
	echo -e 'Non standard arguments detected.' && help_msg
fi
