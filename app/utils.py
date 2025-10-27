from passlib.context import CryptContext #importing CryptContext from passlib.context to hash the password before storing it in the database, this is not used in this code but it is imported so you can use it later on. passlib is a library that allows you to hash passwords and verify them.CryptContext is used to create a context for hashing passwords, it allows you to specify the


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #this is used to create a context for hashing passwords, it allows you to specify the hashing algorithm to use, in this case bcrypt is used, it is a secure hashing algorithm that is widely used for hashing passwords.

def hash(password: str):
    """
    Hash a password using bcrypt.
    :param password: The password to hash.
    :return: The hashed password.
    """
    return pwd_context.hash(password)  # This will hash the password using the bcrypt algorithm and return the hashed password.

def verify(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    :param plain_password: The plain password to verify.
    :param hashed_password: The hashed password to verify against.
    :return: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)  # This will verify the plain password against the hashed password and return True if they match, False otherwise.