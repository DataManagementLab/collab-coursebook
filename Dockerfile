FROM python:alpine

#WKHTMLToPDF is not in the newer alpine repos anymore
FROM surnet/alpine-wkhtmltopdf:3.16.2-0.12.6-full as wkhtmltopdf
RUN apk add --no-cache \
        libstdc++ libx11 libxrender libxext libssl1.1 ca-certificates \
        fontconfig freetype ttf-droid ttf-freefont ttf-liberation;
# wkhtmltopdf copy bins from ext image
COPY --from=wkhtmltopdf /bin/wkhtmltopdf /bin/libwkhtmltox.so /bin/

# Add the dependencies for the collab-coursebook
RUN apk add --no-cache \
		 bash poppler libmagic gettext texlive-full py3-virtualenv gcc g++;

#COPY ./requirements.txt .
RUN pip install ./requirements.txt

# Set the working directory
WORKDIR /app

# Expose port 8000
EXPOSE 8000

CMD 
