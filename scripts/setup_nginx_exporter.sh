#!/bin/bash
source ./common.env

for ip in ${BACKEND1_IP} ${BACKEND2_IP} ${BACKEND3_IP}; do
  ssh ${USER}@${ip} <<'EOF'
  wget -q https://github.com/nginx/nginx-prometheus-exporter/releases/download/v1.4.2/nginx-prometheus-exporter_1.4.2_linux_amd64.tar.gz
  tar -xzf nginx-prometheus-exporter_1.4.2_linux_amd64.tar.gz
  sudo mv nginx-prometheus-exporter /usr/local/bin/
  sudo useradd -rs /bin/false nginx_exporter || true
  sudo tee /etc/systemd/system/nginx-prometheus-exporter.service > /dev/null <<EOL
[Unit]
Description=Nginx Prometheus Exporter
After=network.target

[Service]
Type=simple
User=www-data
ExecStart=/usr/local/bin/nginx-prometheus-exporter \
  -nginx.scrape-uri http://127.0.0.1/nginx_status
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOL
  sudo systemctl daemon-reload
  sudo systemctl enable nginx-prometheus-exporter
  sudo systemctl start nginx-prometheus-exporter
EOF
done

echo "nginx-prometheus-exporter installation and service setup completed on all backends." 