# services/transaction_service.py
import uuid
from django.utils import timezone

from walletservice.models import DigitalWallet
from cardservice.services import AcquirerConnector
from cardservice.models import Transaction


class TransactionService:
    def process_payment(self, user, card, amount):
        txn_ref = f'TXN-{uuid.uuid4().hex}'
        txn = Transaction.objects.create(user=user, card=card, amount=amount, transaction_reference=txn_ref)
        response = AcquirerConnector().charge_card(card.card_token, amount, txn_ref)

        if response['status'] == 'APPROVED':
            txn.status = 'SUCCESS'
            txn.completed_at = timezone.now()
            txn.external_reference = response['external_reference']
            txn.save()

            wallet = DigitalWallet.objects.get(user=user)
            wallet.balance += amount
            wallet.save()

        else:
            txn.status = 'FAILED'
            txn.completed_at = timezone.now()
            txn.save()

        return txn