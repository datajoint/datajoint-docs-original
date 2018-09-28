pip3 install -r requirements.txt
make site
which xelatex \
	&& make latexpdf LATEXMKOPTS="-xelatex" \
	|| echo "skipping pdf build: xelatex not installed"
