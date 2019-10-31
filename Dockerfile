FROM nbgallery/jupyter-alpine:7.8.4

RUN \
  apk add texlive-full imagemagick ghostscript-fonts && \
  pip3 install sphinx RunNotebook sphinx_bootstrap_theme recommonmark

RUN \
    mkdir /src && \
    chmod o+rwx /src

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["PROD"]