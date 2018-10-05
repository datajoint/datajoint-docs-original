pip3 install -r requirements.txt
make site
which latex \
	&& make latexpdf \
	|| echo "skipping pdf build: latex not installed"
