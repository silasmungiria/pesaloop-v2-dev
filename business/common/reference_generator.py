import string
import random
import hashlib
from datetime import datetime
from typing import Dict, ClassVar, Optional, Tuple
from django.core.cache import cache

REFERENCE_START_DATE = datetime(2025, 7, 30)
START_YEAR: int = REFERENCE_START_DATE.year

CHARSET: str = string.ascii_uppercase + string.digits
CHARSET_LIST = list(CHARSET)
BASE = len(CHARSET)

class ReferenceGenerator:
    CHARSET: ClassVar[str] = CHARSET
    BASE: ClassVar[int] = BASE
    START_YEAR: ClassVar[int] = START_YEAR

    PREFIXES: ClassVar[Dict[str, str]] = {
        'transaction': 'TXN',
        'fraud_attempt': 'FRD',
        'fraud_rule': 'RUL',
        'model': 'MOD',
        'user': 'USR',
        'wallet': 'WLT',
        'card': 'CRD',
        'payment_request': 'REQ',
        'loan': 'LON',
        'repayment': 'RPM',
        'forex': 'FX',
        'mpesa': 'MPE',
        'batch': 'BCH',
        'refund': 'RFN',
    }

    @classmethod
    def _base_encode(cls, number: int, min_length: int = 1) -> str:
        if number == 0:
            return cls.CHARSET[0] * min_length
        encoded = ''
        while number > 0:
            number, rem = divmod(number, cls.BASE)
            encoded = cls.CHARSET[rem] + encoded
        return encoded.rjust(min_length, cls.CHARSET[0])

    @classmethod
    def _base_decode(cls, encoded: str) -> int:
        number = 0
        for char in encoded:
            number = number * cls.BASE + cls.CHARSET.index(char)
        return number

    @classmethod
    def _encode_timestamp(cls) -> str:
        now = datetime.now()
        year_offset = now.year - cls.START_YEAR

        # Day: A-Z = 1-26, 1-5 = 27-31
        if now.day <= 26:
            day_code = chr(64 + now.day)  # 'A'-'Z'
        else:
            day_code = str(now.day - 26)  # '1'-'5'

        # Hour: A-X = 1-24
        hour_code = chr(64 + now.hour)

        # Minute: base-36 encoded 0–59 -> 2 chars
        minute_code = cls._base_encode(now.minute, 2)

        return (
            cls._base_encode(year_offset, 2) +   # year (2)
            cls._base_encode(now.month, 1) +     # month (1)
            day_code +                           # day (1)
            hour_code +                          # hour (1)
            minute_code                           # minute (2)
        )

    @classmethod
    def _decode_timestamp(cls, ref_part: str) -> Tuple[datetime, int]:
        try:
            encoded_year = ref_part[:2]
            encoded_month = ref_part[2]
            encoded_day = ref_part[3]
            encoded_hour = ref_part[4]
            encoded_minute = ref_part[5:7]

            year = cls.START_YEAR + cls._base_decode(encoded_year)
            month = cls._base_decode(encoded_month)

            # Decode day
            if encoded_day.isalpha():
                day = ord(encoded_day.upper()) - 64
            else:
                day = 26 + int(encoded_day)

            hour = ord(encoded_hour.upper()) - 64
            minute = cls._base_decode(encoded_minute)

            return datetime(year, month, day, hour, minute), 7
        except Exception as e:
            raise ValueError(f"Invalid timestamp encoding: {str(e)}")

    @classmethod
    def _get_sequence_number(cls, prefix: str) -> int:
        key = f"ref_seq_{prefix}_{datetime.now().strftime('%Y%m%d')}"
        try:
            sequence = cache.incr(key)
            if sequence == 1:
                cache.expire(key, 86400)
            return sequence
        except Exception:
            return random.randint(1, 9999)

    @classmethod
    def generate_reference(cls, prefix: str, secure: bool = False) -> str:
        if prefix not in cls.PREFIXES.values():
            raise ValueError(f"Prefix '{prefix}' not registered. Use register_prefix() first.")
        return cls._generate_reference(prefix, secure)

    @classmethod
    def _generate_reference(cls, prefix: str, secure: bool = False) -> str:
        if secure:
            return cls.generate_secure_reference(prefix)
        timestamp = cls._encode_timestamp()
        sequence = cls._base_encode(cls._get_sequence_number(prefix), 3)  # shorter base-36
        return f"{prefix}{timestamp}{sequence}"

    @classmethod
    def generate_secure_reference(cls, prefix: str, secret_data: Optional[str] = None) -> str:
        secret_data = secret_data or str(random.getrandbits(256))
        hash_input = f"{prefix}{cls._encode_timestamp()}{secret_data}"
        digest = hashlib.sha256(hash_input.encode()).hexdigest().upper()
        clean = ''.join(c for c in digest if c in cls.CHARSET)
        return f"{prefix}{clean[:16 - len(prefix)]}"

    @classmethod
    def validate_reference(cls, reference: str, reference_type: Optional[str] = None) -> bool:
        if not reference or not isinstance(reference, str):
            return False
        prefix = cls.PREFIXES.get(reference_type) if reference_type else None
        ref_body = None
        if prefix and reference.startswith(prefix):
            ref_body = reference[len(prefix):]
        elif not prefix:
            for pfx in cls.PREFIXES.values():
                if reference.startswith(pfx):
                    ref_body = reference[len(pfx):]
                    prefix = pfx
                    break
        if not ref_body or len(ref_body) < 10:
            return False
        try:
            cls._decode_timestamp(ref_body)
            return True
        except ValueError:
            return False

    @classmethod
    def get_reference_timestamp(cls, reference: str) -> datetime:
        for prefix in cls.PREFIXES.values():
            if reference.startswith(prefix):
                timestamp_part = reference[len(prefix):]
                dt, _ = cls._decode_timestamp(timestamp_part)
                return dt
        raise ValueError("No known prefix found in reference")

    @classmethod
    def register_prefix(cls, entity_type: str, prefix: str) -> None:
        if not (prefix.isalpha() and prefix.isupper() and 1 <= len(prefix) <= 3):
            raise ValueError("Prefix must be 1-3 uppercase letters")
        cls.PREFIXES[entity_type] = prefix

    # Shortcut methods
    @classmethod
    def transaction_reference(cls, secure=False): return cls._generate_reference(cls.PREFIXES['transaction'], secure)
    @classmethod
    def fraud_reference(cls): return cls._generate_reference(cls.PREFIXES['fraud_attempt'])
    @classmethod
    def fraud_rule_reference(cls): return cls._generate_reference(cls.PREFIXES['fraud_rule'])
    @classmethod
    def model_reference(cls): return cls._generate_reference(cls.PREFIXES['model'])
    @classmethod
    def user_reference(cls): return cls._generate_reference(cls.PREFIXES['user'])
    @classmethod
    def wallet_reference(cls): return cls._generate_reference(cls.PREFIXES['wallet'])
    @classmethod
    def card_reference(cls): return cls._generate_reference(cls.PREFIXES['card'])
    @classmethod
    def payment_request_reference(cls): return cls._generate_reference(cls.PREFIXES['payment_request'])
    @classmethod
    def loan_reference(cls): return cls._generate_reference(cls.PREFIXES['loan'])
    @classmethod
    def repayment_reference(cls): return cls._generate_reference(cls.PREFIXES['repayment'])
    @classmethod
    def forex_reference(cls): return cls._generate_reference(cls.PREFIXES['forex'])
    @classmethod
    def mpesa_reference(cls): return cls._generate_reference(cls.PREFIXES['mpesa'])
    @classmethod
    def batch_reference(cls): return cls._generate_reference(cls.PREFIXES['batch'])
    @classmethod
    def refund_reference(cls): return cls._generate_reference(cls.PREFIXES['refund'])
