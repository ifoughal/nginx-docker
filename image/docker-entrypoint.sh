
# echo "[INFO] Checking if /etc/nginx is deployed"
# if [ -z "$(ls -A /etc/nginx)" ]; then
#   echo "[INFO] /etc/nginx is empty"
#   echo "[INFO] Started deploying configuration to /etc/nginx"
#   cp -a /tmp/nginx/. /etc/nginx/
#   echo "[INFO] Finished deploying configuration to /etc/nginx"
# fi

# echo "[INFO] Started feeding variables default.conf template"
# envsubst "$(printf '${%s} ' $(env | cut -d'=' -f1))"  \
#         < /nginx-config-template/conf.d/default.conf.template \
#         > /etc/nginx/conf.d/default.conf
# echo "[INFO] Finished feeding variables default.conf template"


echo "[INFO] Started generating sites configuration"
config_gen.py
echo "[INFO] Finished generating sites configuration"

# tail -f /dev/null

echo "[INFO] Starting nginx process"
# nginx -g 'daemon off;'
exec "$@"