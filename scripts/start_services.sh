#!/bin/bash
source ./common.env

echo "🚀 Starting all services on VMs..."

# Function to start service if not running
start_service_if_needed() {
    local ip=$1
    local service_name=$2
    local display_name=$3
    
    echo "📡 Checking $display_name on $ip..."
    ssh ${USER}@${ip} <<EOF
if systemctl is-active --quiet $service_name; then
    echo "  ✅ $display_name is already running"
    sudo systemctl status $service_name --no-pager -l | head -5
else
    echo "  🔄 Starting $display_name..."
    sudo systemctl start $service_name
    sudo systemctl status $service_name --no-pager -l | head -5
fi
EOF
}

# Start HAProxy on load balancer
start_service_if_needed ${LOAD_BALANCER_IP} "haproxy" "HAProxy"

# Start Nginx on backend servers
echo "🖥️  Checking Nginx on backend servers..."
for ip in ${BACKEND1_IP} ${BACKEND2_IP} ${BACKEND3_IP}; do
  start_service_if_needed $ip "nginx" "Nginx"
done

# Start Node Exporter on all VMs (if monitoring is set up)
echo "📊 Checking Node Exporter on all VMs..."
for ip in ${LOAD_BALANCER_IP} ${BACKEND1_IP} ${BACKEND2_IP} ${BACKEND3_IP} ${CLIENT_IP}; do
  start_service_if_needed $ip "node_exporter" "Node Exporter"
done

# Start Prometheus and Grafana on monitoring host (if set up)
if [ ! -z "${PROMETHEUS_HOST}" ]; then
  echo "📈 Checking Prometheus and Grafana on monitoring host..."
  start_service_if_needed ${PROMETHEUS_HOST} "prometheus" "Prometheus"
  start_service_if_needed ${PROMETHEUS_HOST} "grafana-server" "Grafana"
fi

echo "✅ All services checked and started!"
echo ""
echo "🔗 Quick access:"
echo "  - Load Balancer: http://${LOAD_BALANCER_IP}:80"
if [ ! -z "${PROMETHEUS_HOST}" ]; then
  echo "  - Grafana: http://${PROMETHEUS_HOST}:3000"
  echo "  - Prometheus: http://${PROMETHEUS_HOST}:9090"
fi
echo ""
echo "🧪 Ready for testing! Use:"
echo "  ./deploy_configs.sh haproxy_rr.cfg  # Switch algorithm"
echo "  ./run_wrk_and_save.sh 100 30s http://${LOAD_BALANCER_IP}/  # Run test" 