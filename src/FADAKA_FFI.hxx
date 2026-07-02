#ifndef FADAKA_FFI_H
#define FADAKA_FFI_H

#include <stdint.h>

#if defined(_WIN32)
#define FADAKA_EXPORT __declspec(dllexport)
#else
#define FADAKA_EXPORT __attribute__((visibility("default")))
#endif

#ifdef __cplusplus
extern "C" {
#endif

// Generates a secure Ed25519 seed/private key pair into the provided buffer
FFI_PLUGIN_EXPORT int32_t fadaka_generate_keypair(uint8_t* out_private_key, uint8_t* out_public_key);

// Signs a transaction payload natively using Ed25519/BLS cryptographic schemes
FFI_PLUGIN_EXPORT int32_t fadaka_sign_transaction(
    const uint8_t* private_key,
    const uint8_t* tx_payload,
    int32_t payload_len,
    uint8_t* out_signature
);

// Starts a local high-performance background node sync loop (Long-running process)
FFI_PLUGIN_EXPORT int32_t fadaka_initialize_node_loop(const char* node_config_json);

#ifdef __cplusplus
}
#endif

#endif // FADAKA_FFI_H
