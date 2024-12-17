import os
from dotenv import load_dotenv
import logging
import sys
import boto3

from kms import KeyManagementService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

required_env_vars = [
    "AWS_DEFAULT_REGION",
    "KMS_ALIAS",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "MFA_SERIAL",
]


def load_env() -> dict:
    load_dotenv()

    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Return the environment variables as a dictionary
    return {var: os.getenv(var) for var in required_env_vars}


# access sts to get temporary security token.
def get_security_token(access_key, secret_key, mfa_name, mfa_code, duration=3600):
    sts_client = boto3.client(
        'sts',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    # get temporary credentials
    response = sts_client.get_session_token(DurationSeconds=duration, SerialNumber=mfa_name, TokenCode=mfa_code)

    credentials = response['Credentials']
    logging.info("Temporary Security Credentials Retrieved:")
    logging.info(f"Access Key: {credentials['AccessKeyId']}")
    logging.info(f"Secret Key: {credentials['SecretAccessKey']}")
    logging.info(f"Session Token: {credentials['SessionToken']}")

    return credentials


def main():
    # load environment variables and check if required variables are set
    env_variables = load_env()

    # get mfa things
    mfa_code = sys.argv[1]
    mfa_name = env_variables['MFA_SERIAL']

    # get temporary credentials using mfa
    credentials = get_security_token(env_variables['AWS_ACCESS_KEY_ID'], env_variables['AWS_SECRET_ACCESS_KEY'], mfa_name, mfa_code)
    
    # setup KMS client
    kms = KeyManagementService.from_client(env_variables['AWS_DEFAULT_REGION'], credentials)

    # Test data
    data = "This is a test message."
    logging.info(f"Original data: {data}")

    ### Encrypt and decrypt
    encrypted_data = kms.encrypt(env_variables['KMS_ALIAS'], data)
    # logging.info(f"Encrypted data: {encrypted_data}")

    decrypted_data = kms.decrypt(encrypted_data)
    # logging.info(f"Decrypted data: {decrypted_data}")


if __name__ == '__main__':
    main()