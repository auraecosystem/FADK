use sha2::{Digest, Sha256};
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone)]
struct Transaction {
    from: String,
    to: String,
    amount: u64,
}

#[derive(Debug, Clone)]
struct Block {
    index: u64,
    timestamp: u128,
    transactions: Vec<Transaction>,
    previous_hash: String,
    nonce: u64,
    miner: String,
    hash: String,
}

#[derive(Debug)]
struct Blockchain {
    chain: Vec<Block>,
    difficulty: usize,
    mining_reward: u64,
}

impl Blockchain {

    // ------------------------------------------------
    // Initialize blockchain
    // ------------------------------------------------

    fn new(owner_wallet: String) -> Self {

        let genesis = Blockchain::create_genesis_block(owner_wallet);

        Blockchain {
            chain: vec![genesis],
            difficulty: 4,
            mining_reward: 50,
        }
    }

    // ------------------------------------------------
    // Genesis Block
    // ------------------------------------------------

    fn create_genesis_block(owner_wallet: String) -> Block {

        let tx = Transaction {
            from: "GENESIS".to_string(),
            to: owner_wallet.clone(),
            amount: 1_000_000,
        };

        let timestamp = current_timestamp();

        let mut genesis = Block {
            index: 0,
            timestamp,
            transactions: vec![tx],
            previous_hash: "0".to_string(),
            nonce: 0,
            miner: owner_wallet,
            hash: String::new(),
        };

        genesis.hash = Blockchain::calculate_hash(&genesis);

        genesis
    }

    // ------------------------------------------------
    // Hash Block
    // ------------------------------------------------

    fn calculate_hash(block: &Block) -> String {

        let data = format!(
            "{}{:?}{}{}{}{}",
            block.index,
            block.transactions,
            block.timestamp,
            block.previous_hash,
            block.nonce,
            block.miner
        );

        let mut hasher = Sha256::new();

        hasher.update(data);

        format!("{:x}", hasher.finalize())
    }

    // ------------------------------------------------
    // Mine Block
    // ------------------------------------------------

    fn mine_block(
        &self,
        mut block: Block,
    ) -> Block {

        let target = "0".repeat(self.difficulty);

        loop {

            block.hash = Blockchain::calculate_hash(&block);

            if block.hash.starts_with(&target) {
                println!(
                    "⛏️ Block mined: {}",
                    block.hash
                );

                return block;
            }

            block.nonce += 1;
        }
    }

    // ------------------------------------------------
    // Add Block
    // ------------------------------------------------

    fn add_block(
        &mut self,
        transactions: Vec<Transaction>,
        miner_address: String,
    ) {

        let reward_tx = Transaction {
            from: "NETWORK".to_string(),
            to: miner_address.clone(),
            amount: self.mining_reward,
        };

        let mut txs = transactions;

        txs.push(reward_tx);

        let previous_block =
            self.chain.last().unwrap();

        let block = Block {
            index: self.chain.len() as u64,
            timestamp: current_timestamp(),
            transactions: txs,
            previous_hash: previous_block.hash.clone(),
            nonce: 0,
            miner: miner_address,
            hash: String::new(),
        };

        let mined = self.mine_block(block);

        self.chain.push(mined);
    }

    // ------------------------------------------------
    // Validate Chain
    // ------------------------------------------------

    fn is_valid(&self) -> bool {

        for i in 1..self.chain.len() {

            let current = &self.chain[i];
            let previous = &self.chain[i - 1];

            let recalculated =
                Blockchain::calculate_hash(current);

            if current.hash != recalculated {
                return false;
            }

            if current.previous_hash != previous.hash {
                return false;
            }
        }

        true
    }

    // ------------------------------------------------
    // Print Chain
    // ------------------------------------------------

    fn print_chain(&self) {

        for block in &self.chain {

            println!("{:#?}", block);
        }
    }
}

// ----------------------------------------------------
// Wallet
// ----------------------------------------------------

#[derive(Debug)]
struct Wallet {
    address: String,
}

impl Wallet {

    fn new(address: &str) -> Self {

        Wallet {
            address: address.to_string(),
        }
    }
}

// ----------------------------------------------------
// Timestamp Helper
// ----------------------------------------------------

fn current_timestamp() -> u128 {

    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_millis()
}

// ----------------------------------------------------
// Main
// ----------------------------------------------------

fn main() {

    println!("🚀 Starting Fadaka Blockchain");

    let genesis_owner =
        Wallet::new("KUBU_LEE_GENESIS");

    let miner =
        Wallet::new("FADAKA_MINER_001");

    let mut blockchain =
        Blockchain::new(
            genesis_owner.address.clone()
        );

    println!("✅ Genesis block created");

    let tx1 = Transaction {
        from: genesis_owner.address.clone(),
        to: "USER_A".to_string(),
        amount: 2500,
    };

    blockchain.add_block(
        vec![tx1],
        miner.address.clone(),
    );

    println!(
        "✅ Blockchain valid: {}",
        blockchain.is_valid()
    );

    blockchain.print_chain();
}
