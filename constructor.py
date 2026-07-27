from eth_abi import encode

def encode_constructor_args(types: list[str], values: list) -> str:
    """Encodes constructor arguments to match the trailing deployment payload."""
    try:
        # Strict encoding to match EVM ABI specifications
        encoded_bytes = encode(types, values)
        return encoded_bytes.hex()
    except Exception as e:
        raise ValueError(f"ABI Encoding failed: {str(e)}")

# Example Output:
# types = ['address', 'uint256']
# values = ['0x1234567890123456789012345678901234567890', 100]
# Returns: 00000000000000000000000012345678901234567890123456789012345678900000000000000000000000000000000000000000000000000000000000000064
