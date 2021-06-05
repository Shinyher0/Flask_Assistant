if [ "$1" = "build" ]; then
	make clean && make html
elif [ "$1" = "api" ]; then
	sphinx-apidoc -f -o ./source ../flask_assistant
else
	echo "Command: '$1' not found"
fi
