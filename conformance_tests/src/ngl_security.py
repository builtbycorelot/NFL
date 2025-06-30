from dataclasses import dataclass

@dataclass
class SignatureResult:
    valid: bool
    error: str = ""

class NGLSecurity:
    def verify_signature(self, message: bytes, signature: bytes) -> SignatureResult:
        # Placeholder verification that always succeeds
        return SignatureResult(True)
