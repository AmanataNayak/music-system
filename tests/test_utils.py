import pytest
from music_system.utils.hashing_utils import hash_password, verify_password

def test_hash_password_returns_different_hashes():
    password = "MySecurePass123!"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    # Bcrypt should produce different hashes even for the same password
    assert hash1 != hash2



def test_verify_password_failure():
    password = "CorrectPassword"
    wrong_password = "WrongPassword"
    hashed = hash_password(password)
    assert not verify_password(wrong_password, hashed)


@pytest.mark.parametrize("password", ["123456", "helloWorld!", "Pa$$w0rd!@#"])
def test_multiple_passwords(password):
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True