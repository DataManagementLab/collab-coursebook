FROM alpine:3.19.0

# Add the dependencies for the collab-coursebook
RUN apk add --no-cache \
		 python3 py3-pip bash poppler libmagic gettext texlive-full py3-virtualenv gcc g++ build-base jpeg-dev zlib-dev;

# Install packages not yet updated for the current alpine version TODO remove when no longer needed
RUN echo 'https://dl-cdn.alpinelinux.org/alpine/v3.14/community' >> /etc/apk/repositories
RUN echo 'https://dl-cdn.alpinelinux.org/alpine/v3.14/main' >> /etc/apk/repositories
RUN apk add --no-cache wkhtmltopdf

#RUN virtualenv venv -p python3
ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY ./requirements.txt ./
COPY ./dockerStartupScript.sh ./
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip install --no-cache-dir --upgrade setuptools pip wheel \
	&& pip install --no-cache-dir -r requirements.txt

# Set the working directory, here is the dev folder to be mounted
WORKDIR /app

# Expose port 8000
EXPOSE 8000

ENTRYPOINT ["python", "./manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
