# services/tokenization_service.py
import uuid

class TokenizationService:
    @staticmethod
    def tokenize_card(card_number, expiry_month, expiry_year, cvv):
        token = uuid.uuid4().hex
        last_four = card_number[-4:]
        card_type = 'VISA' if card_number.startswith('4') else 'OTHER'
        return {
            'token': token,
            'last_four': last_four,
            'card_type': card_type
        }