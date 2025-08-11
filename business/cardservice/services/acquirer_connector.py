# services/acquirer_connector.py
class AcquirerConnector:
    def charge_card(self, card_token, amount, transaction_ref):
        if amount <= 500000:
            return {
                'status': 'APPROVED',
                'external_reference': f'PROC-{transaction_ref[:8]}'
            }
        else:
            return {
                'status': 'DECLINED',
                'reason': 'Exceeds limit'
            }
