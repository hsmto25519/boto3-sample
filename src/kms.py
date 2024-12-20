import boto3
import logging

logger = logging.getLogger(__name__)

CHARACTER_ENCODING = "utf-8"
ENCRYPTION_CONTEXT = { "System": "Test" }

# no error handling for simplicity
class KeyManagementService:
    def __init__(self, kms_client):
        self.kms_client = kms_client

    @classmethod
    def from_client(cls, region_name, credentials) -> "KeyManagementService":
        """
        Creates a KeyManagementService instance with a default KMS client.

        :return: An instance of KeyManagementService initialized with the default KMS client.
        """
        
        kms_client = boto3.client(
            "kms",
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name=region_name
        )

        return cls(kms_client)


    def encrypt(self, key_id: str, text: str) -> str:
        response = self.kms_client.encrypt(KeyId=key_id, Plaintext=text.encode(CHARACTER_ENCODING), EncryptionContext=ENCRYPTION_CONTEXT)
        logger.info(f"The string was encrypted with algorithm {response['EncryptionAlgorithm']}")
        logging.info(f"Encrypted data: {response["CiphertextBlob"]}")

        return response["CiphertextBlob"]


    def decrypt(self, ciphertext: bytes) -> str:
        response = self.kms_client.decrypt(CiphertextBlob=ciphertext, EncryptionContext=ENCRYPTION_CONTEXT)
        plaintext = response["Plaintext"].decode(CHARACTER_ENCODING)
        logger.info(f"Decrypted data: {plaintext}")

        return plaintext