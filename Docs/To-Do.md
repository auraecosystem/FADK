# **🚀 FADAKA DEPLOYMENT STRATEGY - Making It Live**

## **Current Status Assessment**

### ✅ **What's Ready**
- **Docker containerization** → Build/deployment infrastructure in place
- **Hardhat config** → Smart contracts ready for compilation & deployment
- **Go/Node implementations** → Backend services configured
- **Environment files** → `.env` and `.env.development` ready
- **Package managers** → npm, pnpm, go.mod all configured

### ⚠️ **What Needs Attention**
- **Missing implementation files** (placeholders detected)
- **Repository disorganization** (command-line artifacts as files)
- **No CI/CD pipeline active**
- **Database/storage not configured**
- **Networking ports not fully mapped**

---

## **PHASE 1: Foundation Setup (Week 1)**

### **1.1 Clean Up Repository Structure**

```bash.zsh
# Remove command-line artifacts that shouldn't be files
git rm "brew services start fadaka-node"
git rm "go mod tidy"
git rm "make all"
git rm "pnpm install"
git rm "pnpm dev"
# ... etc

# Properly organize directories
mkdir -p {node_modules,build,artifacts,data,logs}
```

### **1.2 Set Up Environment Variables**

```bash.zsh
# Copy and configure .env for production
cp .env.development .env.production

# Required variables:
FADAKA_PRIVATE_KEY=your_private_key_here
FADAKA_TESTNET_RPC=http://localhost:8545
FADAKA_MAINNET_RPC=https://mainnet-rpc.fadakablockchain.com
FADAKA_EXPLORER_API_KEY=your_api_key
DATABASE_URL=postgres://user:pass@localhost/fadaka
NODE_ENV=production
```

### **1.3 Install Dependencies**

```bash.zsh
# Frontend/Node dependencies
npm install
pnpm install
hardhat compile

# Go dependencies
go mod download
go mod tidy

# Python dependencies (for utilities)
pip install -r requirements.txt
```

---

## **PHASE 2: Build & Containerize (Week 2)**

### **2.1 Build Docker Images**

```dockerfile
# Multi-stage build (Already configured in root Dockerfile)
docker build -t fadaka-node:latest -f Dockerfile .

# Optional: Build API service separately
docker build -t fadaka-api:latest -f Dockerfile.alltools --target api .
```

### **2.2 Set Up Docker Compose**

Create/complete `docker-compose.yml`:

```yaml
version: '3.8'
services:
  # ────────────────────────────────────────
  # Blockchain Node
  # ────────────────────────────────────────
  fadaka-node:
    image: fadaka-node:latest
    container_name: fadaka-node
    ports:
      - "30303:30303"  # P2P
      - "8545:8545"    # RPC HTTP
      - "8546:8546"    # WebSocket
    environment:
      - FADAKA_NETWORK=mainnet
      - FADAKA_VALIDATOR=true
      - LOG_LEVEL=info
    volumes:
      - ./data:/app/data
      - ./config.toml:/app/config.toml
    networks:
      - fadaka-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8545"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ────────────────────────────────────────
  # Smart Contract API
  # ────────────────────────────────────────
  fadaka-api:
    image: fadaka-api:latest
    container_name: fadaka-api
    ports:
      - "8000:8000"
    environment:
      - RPC_URL=http://fadaka-node:8545
      - DATABASE_URL=postgresql://postgres:password@db:5432/fadaka
    depends_on:
      - fadaka-node
      - db
    networks:
      - fadaka-network
    restart: unless-stopped

  # ────────────────────────────────────────
  # PostgreSQL Database
  # ────────────────────────────────────────
  db:
    image: postgres:15-alpine
    container_name: fadaka-db
    environment:
      - POSTGRES_DB=fadaka
      - POSTGRES_PASSWORD=secure_password_here
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - fadaka-network
    restart: unless-stopped

  # ────────────────────────────────────────
  # Indexer (Logstash) - For logs
  # ────────────────────────────────────────
  logstash:
    image: docker.elastic.co/logstash/logstash:8.0.0
    container_name: fadaka-logstash
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    environment:
      - "ES_JAVA_OPTS=-Xms256m -Xmx256m"
    ports:
      - "9600:9600"
    networks:
      - fadaka-network

networks:
  fadaka-network:
    driver: bridge

volumes:
  postgres_data:
```

### **2.3 Deploy with Docker Compose**

```bash
# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps

# Check logs
docker-compose logs -f fadaka-node
```

---

## **PHASE 3: Smart Contracts Deployment (Week 2)**

### **3.1 Configure Hardhat**

```javascript
// hardhat.config.js - updated
module.exports = {
  solidity: "0.8.21",
  networks: {
    fadakaTestnet: {
      url: process.env.FADAKA_TESTNET_RPC || "http://localhost:8545",
      accounts: [process.env.FADAKA_PRIVATE_KEY],
      chainId: 1001
    },
    fadakaMainnet: {
      url: process.env.FADAKA_MAINNET_RPC,
      accounts: [process.env.FADAKA_PRIVATE_KEY],
      chainId: 1000
    }
  },
  etherscan: {
    apiKey: process.env.FADAKA_EXPLORER_API_KEY
  }
};
```

### **3.2 Deploy Core Contracts**

```bash
# Compile contracts
npx hardhat compile

# Deploy to testnet
npx hardhat run scripts/deploy.js --network fadakaTestnet

# Verify contracts
npx hardhat verify --network fadakaTestnet CONTRACT_ADDRESS "constructor args"
```

**Deploy order:**
1. `Safemath.sol` (utilities)
2. `IDepositContract.sol` (staking)
3. `Lola.sol` (token)
4. `FusionBridge.sol` (cross-chain)
5. `Unswapairv2.sol` (DEX)

---

## **PHASE 4: Frontend Deployment (Week 3)**

### **4.1 Build Vue Frontend**

```bash
# Install dependencies
npm install

# Build for production
npm run build

# Output in dist/ directory
```

### **4.2 Deploy via Vercel/Netlify**

```bash
# Option A: Vercel (recommended)
npm install -g vercel
vercel --prod

# Option B: Netlify
netlify deploy --prod --dir=dist
```

### **4.3 Configure Web3Auth Integration**

```typescript
// Update App.vue with production credentials
const web3AuthContextConfig = {
  appName: "Fadaka",
  clientId: process.env.VUE_APP_WEB3AUTH_CLIENT_ID,
  network: "mainnet",
  redirectUrl: "https://fadaka.example.com"
};
```

---

## **PHASE 5: Node Operations (Week 3-4)**

### **5.1 Initialize Testnet**

```bash
# Generate validator keys
./fadaka-node genkey

# Create genesis block
./fadaka-node init-genesis --validators=100 --supply=1000000000

# Start validator node
./fadaka-node --validator --datadir=./data --http --http.port=8545
```

### **5.2 Configure Validator**

```toml
# config.toml
[validator]
enabled = true
voting_power = 100
min_stake = "1000000000000000000"  # 1 FADK

[consensus]
consensus_timeout = "1.5s"
max_validators = 100

[network]
p2p_port = 30303
http_port = 8545
websocket_port = 8546

[storage]
database_path = "./data/db"
```

### **5.3 Monitor Node Health**

```bash
# Check node status
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

# Monitor logs
docker-compose logs -f fadaka-node --tail=100
```

---

## **PHASE 6: Network & Security (Week 4)**

### **6.1 Configure Reverse Proxy**

```nginx
# nginx.conf
upstream fadaka_node {
    server fadaka-node:8545;
}

upstream fadaka_api {
    server fadaka-api:8000;
}

server {
    listen 443 ssl http2;
    server_name fadaka.example.com;

    ssl_certificate /etc/letsencrypt/live/fadaka.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/fadaka.example.com/privkey.pem;

    # RPC endpoint
    location /rpc {
        proxy_pass http://fadaka_node;
        proxy_http_version 1.1;
        proxy_set_header Connection "upgrade";
    }

    # API
    location /api {
        proxy_pass http://fadaka_api;
    }
}
```

### **6.2 Enable HTTPS**

```bash
# Using Certbot
certbot certonly --standalone -d fadaka.example.com

# Auto-renewal
certbot renew --dry-run
```

### **6.3 Security Hardening**

```bash
# Firewall rules
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw allow 30303/tcp # P2P
ufw enable

# Update system
apt-get update && apt-get upgrade -y

# Install monitoring
docker run -d \
  -p 9090:9090 \
  -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

---

## **PHASE 7: Testing & Launch (Week 4-5)**

### **7.1 Integration Tests**

```bash
# Test blockchain RPC
npx hardhat test

# Test smart contracts
npx hardhat test --network fadakaTestnet

# Load testing
ab -n 1000 -c 10 http://localhost:8000/api/health
```

### **7.2 Testnet Launch Checklist**

- [ ] Nodes syncing correctly
- [ ] Smart contracts deployed & verified
- [ ] Frontend loading without errors
- [ ] Wallet integration working
- [ ] Transaction signing working
- [ ] Block explorer operational
- [ ] Monitoring alerts configured

### **7.3 Mainnet Launch Checklist**

- [ ] Security audit complete
- [ ] Validator set finalized
- [ ] Genesis block created
- [ ] Backup systems operational
- [ ] Emergency procedures documented
- [ ] Support team trained

---

## **OPERATIONAL COMMANDS**

```bash
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
```

---

## **ESTIMATED TIMELINE**

| Phase | Tasks | Duration |
|-------|-------|----------|
| **1** | Setup, cleanup, env config | 3-5 days |
| **2** | Docker build, compose | 3-4 days |
| **3** | Smart contract deployment | 4-5 days |
| **4** | Frontend build & deploy | 3-4 days |
| **5** | Node operations & monitoring | 5-7 days |
| **6** | Networking & security | 4-5 days |
| **7** | Testing & launch | 5-7 days |
| **TOTAL** | | **4-5 weeks** |

---

## **KEY DELIVERABLES FOR LIVE DEPLOYMENT**

✅ **Running blockchain nodes** (mainnet + testnet)  
✅ **Deployed smart contracts**  
✅ **Live frontend (Web3Auth enabled)**  
✅ **REST/gRPC API endpoints**  
✅ **Block explorer**  
✅ **Wallet integrations**  
✅ **Monitoring & alerting**  
✅ **24/7 Support infrastructure**  

