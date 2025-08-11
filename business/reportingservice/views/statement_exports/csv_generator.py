import csv
from io import StringIO
from django.http import HttpResponse
from .email_handler import create_email_subject_and_message, send_email_with_attachment


def generate_csv_report(transactions, request, filename, email=False):
    if email:
        buffer = StringIO()
        writer = csv.writer(buffer)
        write_csv_content(writer, transactions)

        subject, message = create_email_subject_and_message(request.user, filename)
        send_email_with_attachment(
            to_email=request.user.email,
            subject=subject,
            body=message,
            attachment=buffer.getvalue().encode('utf-8'),
            filename=filename,
            mimetype="text/csv"
        )
        return {"message": "CSV report sent via email successfully."}

    else:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        write_csv_content(writer, transactions)
        return response


def write_csv_content(writer, transactions):
    metadata_keys, stk_callback_keys, body_keys, callback_metadata_keys = set(), set(), set(), set()

    for transaction in transactions:
        if transaction.metadata:
            metadata_keys.update(transaction.metadata.keys())
            body = transaction.metadata.get("Body", {})
            if body:
                body_keys.update(body.keys())
                stk_callback = body.get("stkCallback", {})
                if stk_callback:
                    stk_callback_keys.update(stk_callback.keys())
                    callback_metadata = stk_callback.get("CallbackMetadata", {})
                    for item in callback_metadata.get("Item", []):
                        callback_metadata_keys.add(item.get("Name", ""))

    metadata_keys, stk_callback_keys, body_keys, callback_metadata_keys = map(sorted, [metadata_keys, stk_callback_keys, body_keys, callback_metadata_keys])

    headers = [
        'Transaction Reference ID', 'Sender Name', 'Sender Account Number',
        'Recipient Name', 'Recipient Account Number', 'Currency',
        'Transaction Amount', 'Transaction Fee', 'Transaction Status',
        'Date Created', 'Date Updated'
    ]
    headers += [f"Metadata: {key}" for key in metadata_keys]
    headers += [f"Body: {key}" for key in body_keys]
    headers += [f"stkCallback: {key}" for key in stk_callback_keys]
    headers += [f"CallbackMetadata: {key}" for key in callback_metadata_keys]

    writer.writerow(headers)

    for txn in transactions:
        row = [
            txn.reference_id,
            txn.sender_wallet.wallet_owner.get_full_name() if txn.sender_wallet else 'N/A',
            txn.sender_wallet.wallet_owner.account_number if txn.sender_wallet else 'N/A',
            txn.receiver_wallet.wallet_owner.get_full_name() if txn.receiver_wallet else 'N/A',
            txn.receiver_wallet.wallet_owner.account_number if txn.receiver_wallet else 'N/A',
            txn.currency, txn.amount, txn.transaction_charge,
            txn.status.title().replace("_", " "),
            txn.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            txn.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        ]
        metadata = txn.metadata or {}
        row.extend(metadata.get(key, 'N/A') for key in metadata_keys)

        body = metadata.get("Body", {})
        row.extend(body.get(key, 'N/A') for key in body_keys)

        stk_callback = body.get("stkCallback", {}) if body else {}
        row.extend(stk_callback.get(key, 'N/A') for key in stk_callback_keys)

        callback_metadata = stk_callback.get("CallbackMetadata", {}) if stk_callback else {}
        for key in callback_metadata_keys:
            value = 'N/A'
            for item in callback_metadata.get("Item", []):
                if item.get("Name") == key:
                    value = item.get("Value", 'N/A')
                    break
            row.append(value)

        writer.writerow(row)
