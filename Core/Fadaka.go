package verification

import (
	"bytes"
	"context"
	"encoding/binary"
	"encoding/hex"
	"errors"
	"fmt"

	"://github.com"
	"://github.com"
)

// Engine orchestrates low-level bytecode auditing on the Fadaka network.
type Engine struct {
	client *ethclient.Client
}

// NewEngine initializes the validation controller.
func NewEngine(rpcURL string) (*Engine, error) {
	client, err := ethclient.Dial(rpcURL)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to Fadaka RPC: %w", err)
	}
	return &Engine{client: client}, nil
}

// StripCBORMetadata isolates execution bytecode by removing the trailing compiler metadata hash.
func (e *Engine) StripCBORMetadata(bytecode []byte) []byte {
	length := len(bytecode)
	if length < 2 {
		return bytecode
	}

	// Read the last 2 bytes acting as the CBOR length indicator (Big Endian)
	cborLength := binary.BigEndian.Uint16(bytecode[length-2:])

	// Boundary check to ensure it's a valid metadata block
	if int(cborLength)+2 > length {
		return bytecode
	}

	// Slice off the trailing metadata payload
	return bytecode[:length-int(cborLength)-2]
}

// VerifyContract checks an on-chain deployment against target compile data.
func (e *Engine) VerifyContract(ctx context.Context, contractAddr string, localBytecodeHex string) (bool, error) {
	address := common.HexToAddress(contractAddr)
	
	// 1. Fetch live execution code from state database
	onChainBytecode, err := e.client.CodeAt(ctx, address, nil)
	if err != nil {
		return false, fmt.Errorf("failed to fetch state bytecode: %w", err)
	}
	if len(onChainBytecode) == 0 {
		return false, errors.New("target address contains no code (EOA or self-destructed)")
	}

	// 2. Decode local compiler output
	localBytecode, err := hex.DecodeString(localBytecodeHex)
	if err != nil {
		return false, fmt.Errorf("invalid local bytecode format: %w", err)
	}

	// 3. Clean both bytecode streams using memory-efficient slicing
	cleanOnChain := e.StripCBORMetadata(onChainBytecode)
	cleanLocal := e.StripCBORMetadata(localBytecode)

	// 4. Perform an optimized cryptographic bytes comparison
	if bytes.Equal(cleanOnChain, cleanLocal) {
		return true, nil
	}

	return false, nil
}
