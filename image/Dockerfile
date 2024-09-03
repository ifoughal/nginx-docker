# Define a default value for the registry
ARG REGISTRY
ARG NGINX_VERSION

######################################################################
# Stage 1: Build the image with initial setup
# Use the ARG value in the FROM instruction
FROM ${REGISTRY:+${REGISTRY}/}nginxinc/nginx-unprivileged:${NGINX_VERSION} as builder
######################################################################
USER nginx
# Run Nginx initially to generate /etc/nginx structure
RUN nginx && sleep 5 && nginx -s quit
######################################################################
COPY ./sites.yaml /etc/nginx/sites.yaml
COPY ./templates/* /etc/nginx/conf.d/
######################################################################
# Stage 2: Final image with volumes mounted
FROM ${REGISTRY:+${REGISTRY}/}nginxinc/nginx-unprivileged:${NGINX_VERSION} as final
# Copy the generated Nginx configuration and certificates
COPY --from=builder /etc/nginx /etc/nginx
RUN mkdir -p /etc/nginx/ssl
USER root
# from base as with_sources_list
# COPY sources.list /etc/apt/sources.list
# RUN apt update; exit 0
######################################################################
# from base as with_debug_tools
RUN apt update && \
    apt install \
        curl net-tools iputils-ping ncurses-bin \
        vim dnsutils python3 python3-pip python3-venv \
        # python3-certbot-nginx certbot openssl \
        -y
# Create a virtual environment
RUN python3 -m venv /opt/venv
# Activate the virtual environment and install packages
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install pyyaml
######################################################################
COPY ./config_gen.py /usr/local/bin/config_gen.py
# Ensure the script uses the virtual environment's Python
RUN sed -i '1s|^|#!/opt/venv/bin/python3\n|' /usr/local/bin/config_gen.py
RUN chmod +x /usr/local/bin/config_gen.py
######################################################################

# RUN mkdir -p /tmp/nginx/conf.d && mkdir -p /tmp/nginx/ssl/

# RUN chown nginx:nginx -R /tmp/nginx

# RUN cp -a /tmp/nginx/. /etc/nginx/

######################################################################
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
# RUN chown nginx:nginx -R /tmp/nginx

USER nginx

ENTRYPOINT ["/bin/bash", "-c", "source /docker-entrypoint.sh"]
######################################################################
CMD ["/bin/bash", "nginx", "-g", "daemon off;"]
