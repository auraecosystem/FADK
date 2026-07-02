# Start everything
docker-compose -f docker-compose.yml up -d

# Deploy contracts
npm run deploy:testnet
npm run deploy:mainnet

# Monitor
docker-compose logs -f --tail=100

# Restart components
docker-compose restart fadaka-node

# Cleanup
docker-compose down -v

# Backup data
docker exec fadaka-db pg_dump -U postgres fadaka > backup.sql
