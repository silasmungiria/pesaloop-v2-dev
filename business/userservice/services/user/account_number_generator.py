import random


class AccountNumberGenerator:
    @staticmethod
    def generate(length: int = 10, prefix: str = '') -> str:
        """
        Generates a random numeric account number of the specified total length.
        The first digit (after prefix) is guaranteed to be non-zero.

        Args:
            length (int): Total length of the account number including prefix. Default is 10.
            prefix (str): Optional numeric prefix. Default is empty.

        Returns:
            str: Randomly generated account number.
        """
        if length < 1:
            raise ValueError("Account number length must be at least 1")
        if not prefix.isdigit() and prefix != '':
            raise ValueError("Prefix must be numeric")

        remaining_length = length - len(prefix)
        if remaining_length < 1:
            raise ValueError("Length too short for the given prefix")

        first_digit = str(random.randint(1, 9))
        other_digits = ''.join(str(random.randint(0, 9)) for _ in range(remaining_length - 1))
        return prefix + first_digit + other_digits
