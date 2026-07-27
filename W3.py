from web3 import Web3
import solcx

# 1. Compile source locally with identical settings
compiled_sol = solcx.compile_standard({
    "language": "Solidity",
    "sources": {"Contract.sol": {"content": source_code}},
    "settings": {"optimizer": {"enabled": True, "runs": 200}, "outputSelection": {"*": {"*": ["evm.bytecode.object"]}}}
}, solc_version="0.8.20")

local_bytecode = compiled_sol['contracts']['Contract.sol']['MyContract']['evm']['bytecode']['object']

# 2. Fetch deployed bytecode
w3 = Web3(Web3.HTTPProvider("https://fadakachain.network")) # Example RPC
deployed_bytecode = w3.eth.get_code(contract_address).hex()

# 3. Match (Strip metadata for partial matching if necessary)
is_verified = local_bytecode in deployed_bytecode
def strip_solidity_metadata(bytecode_hex: str) -> str:
    """Strips the CBOR metadata tail from Solidity bytecode to isolate execution logic."""
    # Clean string prefix
    if bytecode_hex.startswith("0x"):
        bytecode_hex = bytecode_hex[2:]
        
    bytecode_bytes = bytes.fromhex(bytecode_hex)
    if len(bytecode_bytes) < 2:
        return bytecode_hex

    # Read the last two bytes to find the CBOR length
    cbor_length = int.from_bytes(bytecode_bytes[-2:], byteorder='big')
    
    # Validation safety check (metadata rarely exceeds 100-200 bytes)
    if cbor_length + 2 > len(bytecode_bytes):
        return bytecode_hex
        
    # Slice out the CBOR block and the 2-byte length marker
    execution_bytecode = bytecode_bytes[:-(cbor_length + 2)]
    return execution_bytecode.hex()
