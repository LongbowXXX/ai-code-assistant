#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import os

import boto3
import pytest
from dotenv import load_dotenv


@pytest.mark.skip(reason="just for getting aws session token")
def test_aws_get_session_token() -> None:
    load_dotenv()
    serial_number = os.getenv("AWS_MFA_SERIAL_NUMBER")
    token = os.getenv("AWS_MFA_TOKEN_CODE")
    access_key_id = os.getenv("AWS_MFA_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_MFA_SECRET_ACCESS_KEY")
    client = boto3.client(
        "sts",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )
    response = client.get_session_token(
        DurationSeconds=129600,
        SerialNumber=serial_number,
        TokenCode=token,
    )
    print(f"response={response}")
    access = response["Credentials"]["AccessKeyId"]
    secret = response["Credentials"]["SecretAccessKey"]
    session = response["Credentials"]["SessionToken"]
    print(f"\n\nAWS_ACCESS_KEY_ID='{access}'\nAWS_SECRET_ACCESS_KEY='{secret}'\nAWS_SESSION_TOKEN='{session}'\n\n")
