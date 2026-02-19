#!/bin/bash
#
# Docker Redis Troubleshooting and Fix Script
# Comprehensive solution for Redis container issues
#

set -e

echo "🔧 Docker Redis Troubleshooting Script"
echo "======================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Function to check if Docker is responsive
check_docker_health() {
    echo "🔍 Checking Docker health..."
    if timeout 5 docker version > /dev/null 2>&1; then
        print_status "Docker is responsive"
        return 0
    else
        print_error "Docker is not responding (timeout)"
        return 1
    fi
}

# Function to reset Docker completely
reset_docker() {
    echo ""
    echo "🔄 Resetting Docker..."
    
    # Stop all containers
    echo "   Stopping all containers..."
    docker stop $(docker ps -aq) 2>/dev/null || true
    
    # Remove Redis containers
    echo "   Removing Redis containers..."
    docker rm -f marketing-redis redis-local 2>/dev/null || true
    
    # Remove Redis volumes (optional - data will be lost)
    read -p "   Remove Redis volumes? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker volume rm marketingtvojeinfo_redis_data redis_data 2>/dev/null || true
        print_status "Redis volumes removed"
    else
        print_info "Keeping existing Redis volumes"
    fi
    
    # Clean up networks
    echo "   Cleaning up networks..."
    docker network prune -f 2>/dev/null || true
    
    print_status "Docker reset complete"
}

# Function to start Redis with retry
start_redis() {
    echo ""
    echo "🚀 Starting Redis container..."
    
    local retries=3
    local count=0
    
    while [ $count -lt $retries ]; do
        echo "   Attempt $((count + 1))/$retries..."
        
        if docker-compose up -d redis 2>&1; then
            echo "   Waiting for Redis to be ready..."
            sleep 5
            
            # Test connection
            if docker exec marketing-redis redis-cli -a marketing ping 2>/dev/null | grep -q "PONG"; then
                print_status "Redis is running and responding!"
                return 0
            else
                print_warning "Container started but Redis not responding yet"
                sleep 5
            fi
        else
            print_error "Failed to start container"
        fi
        
        count=$((count + 1))
        if [ $count -lt $retries ]; then
            echo "   Retrying in 5 seconds..."
            sleep 5
        fi
    done
    
    print_error "Failed to start Redis after $retries attempts"
    return 1
}

# Function to check Redis connectivity
check_redis() {
    echo ""
    echo "🔍 Testing Redis connectivity..."
    
    # Check if container is running
    if ! docker ps --filter "name=marketing-redis" --filter "status=running" | grep -q marketing-redis; then
        print_error "Redis container is not running"
        return 1
    fi
    
    # Test with docker exec
    if docker exec marketing-redis redis-cli -a marketing ping 2>/dev/null | grep -q "PONG"; then
        print_status "Redis is responding to PING"
        
        # Test with Node.js
        echo "   Testing with Node.js..."
        if node -e "
            const Redis = require('ioredis');
            const redis = new Redis('redis://:marketing@localhost:36379');
            redis.ping().then(r => {
                console.log('Node.js Redis OK:', r);
                process.exit(0);
            }).catch(e => {
                console.error('Node.js Redis Error:', e.message);
                process.exit(1);
            }).finally(() => redis.disconnect());
        " 2>/dev/null; then
            print_status "Node.js can connect to Redis"
            return 0
        else
            print_warning "Node.js connection failed (might be path issue)"
            return 1
        fi
    else
        print_error "Redis is not responding"
        return 1
    fi
}

# Function to diagnose Docker issues
diagnose_docker() {
    echo ""
    echo "🔍 Diagnosing Docker issues..."
    
    # Check Docker version
    echo "   Docker version:"
    docker version --format '{{.Client.Version}}' 2>/dev/null || echo "   Cannot get version"
    
    # Check if Docker Desktop is running
    echo "   Checking Docker Desktop status..."
    if docker info > /dev/null 2>&1; then
        print_status "Docker daemon is accessible"
    else
        print_error "Cannot connect to Docker daemon"
        print_info "Please ensure Docker Desktop is running"
        return 1
    fi
    
    # Check disk space
    echo "   Checking disk space..."
    docker system df 2>/dev/null || true
    
    # Check for stuck containers
    echo "   Checking for stuck containers..."
    stuck_containers=$(docker ps -aq --filter "status=created" 2>/dev/null | wc -l)
    if [ "$stuck_containers" -gt 0 ]; then
        print_warning "Found $stuck_containers stuck containers"
        print_info "Run 'docker container prune' to clean up"
    fi
    
    return 0
}

# Main menu
show_menu() {
    echo ""
    echo "======================================="
    echo "What would you like to do?"
    echo ""
    echo "1) Full auto-fix (diagnose, reset, start)"
    echo "2) Just diagnose Docker"
    echo "3) Reset Docker and start fresh"
    echo "4) Start Redis container only"
    echo "5) Test Redis connectivity"
    echo "6) Alternative: Use WSL2 Redis instead"
    echo "7) Exit"
    echo ""
    read -p "Select option [1-7]: " choice
    
    case $choice in
        1)
            diagnose_docker
            reset_docker
            start_redis
            check_redis
            ;;
        2)
            diagnose_docker
            ;;
        3)
            reset_docker
            ;;
        4)
            start_redis
            ;;
        5)
            check_redis
            ;;
        6)
            echo ""
            echo "Switching to WSL2 Redis setup..."
            echo "Run this in WSL2:"
            echo "  sudo apt update && sudo apt install redis-server"
            echo "  sudo service redis-server start"
            echo "  sudo redis-cli config set requirepass marketing"
            echo ""
            echo "Then update .env: REDIS_URL=redis://:marketing@localhost:6379"
            ;;
        7)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option"
            show_menu
            ;;
    esac
}

# Main execution
echo ""
if ! check_docker_health; then
    print_error "Docker is not healthy. Please:"
    print_info "1. Restart Docker Desktop"
    print_info "2. Wait for it to fully start"
    print_info "3. Run this script again"
    exit 1
fi

show_menu

echo ""
echo "======================================="
print_status "Script complete!"
echo ""
echo "To verify Redis is working:"
echo "  node scripts/verify-mcp-servers.js"
echo ""
