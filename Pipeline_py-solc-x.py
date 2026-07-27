from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from web3 import Web3
import solcx

app = FastAPI(title="Fadaka Verification Engine")
w3 = Web3(Web3.HTTPProvider("https://fadakachain.network")) # Substitute with real RPC

class VerificationRequest(BaseModel):
    contract_address: str
    source_code: str
    contract_name: str
    compiler_version: str
    optimizer_enabled: bool
    optimizer_runs: int
    constructor_types: list[str] = []
    constructor_args: list = []

def run_verification(req: VerificationRequest):
    # 1. Ensure correct solc binary is installed locally
    if req.compiler_version not in solcx.get_installed_solc_versions():
        solcx.install_solc(req.compiler_version)
        
    # 2. Compile via Standard JSON configuration
    input_json = {
        "language": "Solidity",
        "sources": {"TargetContract.sol": {"content": req.source_code}},
        "settings": {
            "optimizer": {"enabled": req.optimizer_enabled, "runs": req.optimizer_runs},
            "outputSelection": {"*": {"*": ["evm.bytecode.object"]}}
        }
    }
    
    compiled = solcx.compile_standard(input_json, solc_version=req.compiler_version)
    
    # Extract locally compiled runtime bytecode
    local_bytecode = compiled['contracts']['TargetContract.sol'][req.contract_name]['evm']['bytecode']['object']
    
    # 3. Retrieve live on-chain runtime bytecode
    deployed_bytecode = w3.eth.get_code(Web3.to_checksum_address(req.contract_address)).hex()
    
    if deployed_bytecode == "0x" or not deployed_bytecode:
        return {"status": "failed", "reason": "No bytecode found at address"}

    # 4. Strip Metadata from both targets for resilient comparison
    clean_local = strip_solidity_metadata(local_bytecode)
    clean_deployed = strip_solidity_metadata(deployed_bytecode)

    if clean_local == clean_deployed:
        # Update your DB/Explorer state here
        return {"status": "verified", "match_type": "exact_or_partial"}
        
    return {"status": "mismatch"}

@app.post("/api/v1/verify")
async def verify_contract(payload: VerificationRequest):
    # For a production setup, offload this to Celery/Background Tasks
    result = run_verification(payload)
    if result.get("status") == "verified":
        return {"success": True, "message": "Contract successfully verified."}
    raise HTTPException(status_code=400, detail=f"Verification failed: {result.get('reason', 'Bytecode mismatch')}")
