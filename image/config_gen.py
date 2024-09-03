#!/usr/bin/env python3

import yaml
import os
import subprocess
from string import Template


sites_path = '/etc/nginx/sites.yaml'
template_path = '/etc/nginx/conf.d/default.conf.template'


def load_yaml(file_path:str):
    # Load the YAML file
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_file(file_path:str):
    # Load the template file
    with open(file_path, 'r') as template_file:
        return template_file.read()


def write_file(file_path:str, data):
    with open(file_path, 'w') as f:
        f.write(data)


def generate_cert(domain, cert_path, key_path):
    # Generate SSL certificates (self-signed for this example)
    if not os.path.exists(cert_path) or not os.path.exists(key_path):
        subprocess.run([
            "openssl", "req", "-x509", "-nodes", "-days", "365",
            "-newkey", "rsa:2048", "-keyout", key_path,
            "-out", cert_path,
            "-subj", f"/CN={domain}"
        ])


if __name__ == "__main__":
    sites = load_yaml(file_path=sites_path).get('sites', {})
    sites_config = Template(load_file(file_path=template_path))

    for site_name, site_info in sites.items():
        domain = site_info['domain']
        port = site_info['port']

        # Define paths for SSL certificate and key
        cert_path = f"/etc/nginx/ssl/{site_name}.crt"
        key_path = f"/etc/nginx/ssl/{site_name}.key"

        # generating certificates for current site
        generate_cert(domain, cert_path, key_path)

        # Create a dictionary for the template substitution
        # Substitute the template variables with actual values
        nginx_conf = sites_config.safe_substitute({
            'DOMAIN': domain,
            'SITE_NAME': site_name,
            'HOST_ADDRESS': os.environ.get("HOST_ADDRESS", domain),  # defaulting to domain if HOST_ADDRESS not set
            'PORT': str(port)
        })

        file_path = f"/etc/nginx/conf.d/{site_name}.conf"
        # Write the final configuration to a file
        write_file(file_path=file_path, data=nginx_conf)
