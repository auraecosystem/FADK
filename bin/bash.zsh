mkdir -p fdka/platform/darwin/{foundation,security,tls,wallet,bridge}

touch \
fdka/platform/darwin/foundation/corefoundation.go \
fdka/platform/darwin/foundation/corefoundation.s \
fdka/platform/darwin/foundation/cf_array.go \
fdka/platform/darwin/foundation/cf_data.go \
fdka/platform/darwin/foundation/cf_string.go \
fdka/platform/darwin/foundation/cf_dictionary.go \
fdka/platform/darwin/foundation/cf_number.go \
fdka/platform/darwin/foundation/cf_date.go \
fdka/platform/darwin/security/security.go \
fdka/platform/darwin/security/security.s \
fdka/platform/darwin/security/certificate.go \
fdka/platform/darwin/security/trust.go \
fdka/platform/darwin/security/keychain.go \
fdka/platform/darwin/security/identity.go \
fdka/platform/darwin/security/secure_enclave.go \
fdka/platform/darwin/security/biometric.go \
fdka/platform/darwin/security/random.go \
fdka/platform/darwin/tls/tls.go \
fdka/platform/darwin/wallet/wallet.go \
fdka/platform/darwin/bridge/bridge.go \
fdka/platform/darwin/exports.go \
fdka/platform/darwin/types.go
