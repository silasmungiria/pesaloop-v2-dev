# Choices

class ExchangeStatusChoices:
    PROCESSING = 'PROCESSING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'

    CHOICES = [
        (PROCESSING, 'Processing'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
    ]
