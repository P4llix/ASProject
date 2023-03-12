from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

class ECC:
    def __init__(self, key):
        self.key = key
        self.curve = ec.SECP256R1()
        self.algorithm = ec.ECDSA(hashes.SHA256())

        self.priv_key = ec.derive_private_key(self.key, self.curve, default_backend())
        self.pub_key = self.priv_key.public_key()

    def hash(self, data):
        data = b'{data}'
        signature = self.priv_key.sign(data, self.algorithm)
        return '%s' % signature.hex()
