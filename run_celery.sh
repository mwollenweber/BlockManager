#!/usr/bin/env bash
# For OSX development
if [[ `uname` == "Darwin" ]]; then
	script_directory=$(dirname "$0")
fi

# For Linux production deployment
if [[ `uname` == "Linux" ]]; then
	script_directory=$(dirname $(readlink -f $BASH_SOURCE))
fi

if [ -e $script_directory/blockmanager.rc ]
then
	source $script_directory/blockmanager.rc
else
	echo "WARN: $script_directory/blockmanager.rc does not exist."
fi

#celery -A tasks worker

exec $script_directory/env/bin/celery -A reports.tasks worker --loglevel=INFO
