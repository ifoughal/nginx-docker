# Define a default value for the registry
ARG REGISTRY=docker.io
ARG NGINX_VERSION=1.27.1
ARG HTTP_PROXY=
ARG HTTPS_PROXY=
ARG NO_PROXY=

######################################################################
# Stage 1: Build the image with initial setup
# Use the ARG value in the FROM instruction
FROM ${REGISTRY:+${REGISTRY}/}nginxinc/nginx-unprivileged:${NGINX_VERSION} AS builder
######################################################################
USER nginx
# Run Nginx initially to generate /etc/nginx structure
RUN nginx && sleep 5 && nginx -s quit
# ######################################################################
COPY ./sites.yaml /etc/nginx/sites.yaml
COPY ./templates/* /etc/nginx/conf.d/
######################################################################
# Stage 2: Final image with volumes mounted
FROM ${REGISTRY:+${REGISTRY}/}nginxinc/nginx-unprivileged:${NGINX_VERSION} AS forward_proxy
# Copy the generated Nginx configuration and certificates
COPY --from=builder /etc/nginx /etc/nginx
RUN mkdir -p /etc/nginx/ssl
USER root
######################################################################
ENV HTTP_PROXY=$HTTP_PROXY
ENV HTTPS_PROXY=$HTTPS_PROXY
######################################################################
COPY ./00proxy /tmp/00proxy
COPY ./environment /tmp/environment
######################################################################
COPY forward_proxy.sh /tmp/
RUN chmod +x /tmp/forward_proxy.sh
RUN /tmp/forward_proxy.sh

RUN unset HTTP_PROXY
RUN unset HTTPS_PROXY
######################################################################
RUN . /etc/environment
RUN echo "HTTP_PROXY is: ${HTTP_PROXY}"
RUN echo "HTTPS_PROXY is: ${HTTPS_PROXY}"
######################################################################
FROM forward_proxy as final
RUN echo "HTTP_PROXY is: ${HTTP_PROXY}"
RUN echo "HTTPS_PROXY is: ${HTTPS_PROXY}"

######################################################################
# from base as with_debug_tools
RUN apt update -y
RUN apt-get update -y
######################################################################
RUN apt install -y \
        curl net-tools iputils-ping ncurses-bin \
        vim dnsutils python3 python3-pip python3-venv
        # python3-certbot-nginx certbot openssl \
######################################################################
# Create a virtual environment
RUN python3 -m venv /opt/venv
# Activate the virtual environment and install packages
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install pyyaml
######################################################################
COPY ./config_gen.py /usr/local/bin/config_gen.py
# Ensure the script uses the virtual environment's Python
RUN sed -i '1s|^|#!/opt/venv/bin/python3\n|' /usr/local/bin/config_gen.py
RUN chmod +x /usr/local/bin/config_gen.py
######################################################################
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

######################################################################
# clean image from forward_proxy secrets
RUN rm -f /etc/environment && touch /etc/environment
RUN rm -f /etc/apt/apt.conf.d/00proxy

# ENTRYPOINT [ "/bin/sh", "-c", "tail -f /dev/null"]
USER nginx

ENTRYPOINT ["/bin/bash", "-c", "source /docker-entrypoint.sh"]
# ######################################################################
CMD ["/bin/bash", "nginx", "-g", "daemon off;"]
