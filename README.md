# Introduction

Nginx is an open source web server used for serving static or dynamic websites, reverse proxying, load balancing, and other HTTP and proxy server capabilities. It was built to handle large amounts of concurrent connections, and is a popular web server used to host some of the largest and most high-traffic sites on the internet.

Docker is a popular open source containerization tool used to provide a portable and consistent runtime environment for software applications, while consuming less resources than a traditional server or virtual machine. Docker uses containers, isolated user-space environments that run at the operating system level and share system resources such as the kernel and the filesystem.

By containerizing Nginx, it is possible to cut down on some system administration overhead. For instance, you won’t have to manage Nginx through a package manager or build it from source. The Docker container allows you to replace the whole container when a new version of Nginx is released. This way, you only need to maintain the Nginx configuration file and your content.


# Deployment of Nginx:
This compose arch contains all the needed prerequisites to deploy the current stack of container services (Netbox, NetDNS, Jenkins, etc.)
These services have their own docker networks, therefore they are declared in our compose file in order to enable routing, thus reverse proxying the http/https traffic from the host ports 80/443 to the containers.

The Nginx configuration is built from [the template](./nginx/images/templates/default.conf), we then apply the env variables on the template in order to update the host and port addresses.

As long as the port and host are reachable from the Nginx container, then the http traffic will be rerouted accordingly.


# Deployment of new sites:
It is highly preferable to to deploy the sites using a container, thus making the process easier and straightforward.

If you have a static site instead which you wish to deploy through Nginx reverse proxying, then you'll have to bind a volume to the composer. Once the volume is mounted, you have to point to the path to the vol on the Nginx container.

So, first of all, you need to modify the [template](./nginx/images/templates/default.conf) with your service:

Example of service running on a container:
```
server {
    listen 80;
    server_name ${SERVICENAME_FQDN};

    location / {
        set $backend "http://${HOST_ADDRESS}:${SERVICENAME_PORT}";
        proxy_pass $backend;
        # proxy_set_header X-Forwarded-Host $http_host;
        # proxy_set_header X-Real-IP $remote_addr;
        # proxy_set_header X-Forwarded-Proto $scheme;
    }

    access_log off;
    error_log  /var/log/nginx/error.log error;
}
```

The docker-compose of either nginx or your service must be interconnected, either by directly connecting your nginx container to the host:

```yaml
    network_mode: host
```

or by allowing:

```yaml
    cap_add:
        - NET_BIND_SERVICE
```

or by using network connectors:
```yaml
    nginx:
        networks:
        - <SERVICENAME>-con

networks:
    <SERVICENAME>-con:
        external: true
```


Example of a service running on the host:

```
server {
    listen 80;
    server_name ${SERVICENAME_FQDN};

    location / {
        root ${SERVICENAME_ROOT};
        index index.html;
    }

    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    access_log off;
    error_log  /var/log/nginx/error.log error;
}
```

The process of deploying new services has been automated throug config_gen.py with self signed certificates generation.

Once the sites.yaml has been updated, you may rebuild the docker images, or directly modifying the file on the volume and restart the container.

```
docker compose build
```

You may then append your service variables to the [env file](./env/prod.env)

```
sites:
    defguard:
        domain: defguard.arakeen.lan
        port: 8000
```
