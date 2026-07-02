type ApplePlatform interface {
    // Core Foundation
    CreateString(string) (CFStringRef, error)
    CreateData([]byte) (CFDataRef, error)
    Release(any)

    // Certificates
    LoadCertificate([]byte) (Certificate, error)
    VerifyCertificate(Certificate) error
    ExportCertificate(Certificate) ([]byte, error)

    // Trust
    VerifyTrust(Certificate) error

    // Keychain
    StoreKey(string, []byte) error
    LoadKey(string) ([]byte, error)
    DeleteKey(string) error

    // Secure Enclave
    GenerateSecureKey(string) error
    SecureSign(string, []byte) ([]byte, error)
    SecureVerify(string, []byte, []byte) bool

    // Random
    RandomBytes(int) ([]byte, error)
}
