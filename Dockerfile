FROM alpine:3.8 as build-env

WORKDIR /site

#build
ENV HUGO_VERSION=0.30.2
ENV HUGO_DOWNLOAD_URL=https://github.com/spf13/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.tar.gz

RUN apk add --update --no-cache --virtual build-dependencies

# install some build prereqs
RUN apk add --update --no-cache \
		bash \
		build-base \
		ca-certificates \
		curl \
		git \
		libcurl \
		libxml2-dev \
		libxslt-dev \
		openssh \
		rsync \
		ruby \
		ruby-dev \
		wget

# install gems
RUN gem install \
		asciidoctor \
		html-proofer \
		nokogiri \
	--no-document && \
	apk del build-dependencies

# download and install hugo
RUN wget "$HUGO_DOWNLOAD_URL" && \
	tar xzf hugo_${HUGO_VERSION}_Linux-64bit.tar.gz && \
	mv hugo /usr/bin/hugo && \
	rm hugo_${HUGO_VERSION}_Linux-64bit.tar.gz LICENSE.md README.md

#copy the entire website folder into the build environment container
COPY . ./

#actually build the site
RUN hugo

# lets create the actual deployment image
FROM nginx:alpine

#copy over the site config for nginx
COPY ./.docker/default.conf /etc/nginx/conf.d/default.conf

#copy over the built website from the build environment docker
COPY --from=build-env /site/public /usr/share/nginx/html

# we now assume the default nginx container config startups nginx on port 80