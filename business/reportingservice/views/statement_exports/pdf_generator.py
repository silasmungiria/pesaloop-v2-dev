# Third-party library imports
from io import BytesIO
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.lib.pagesizes import LEDGER, portrait

# Project-specific imports
from .email_handler import create_email_subject_and_message, send_email_with_attachment
from .interfaces import NumberedCanvas


def generate_pdf_report(transactions, wallets, request, filename, pdf_view, email=False):
    if email:
        buffer = BytesIO()
        _build_pdf(buffer, transactions, wallets, request, pdf_view)
        subject, message = create_email_subject_and_message(request.user, filename)
        send_email_with_attachment(
            to_email=request.user.email,
            subject=subject,
            body=message,
            attachment=buffer.getvalue(),
            filename=filename,
            mimetype="application/pdf"
        )
        return {"message": "PDF report sent via email successfully."}

    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        _build_pdf(response, transactions, wallets, request, pdf_view)
        return response


def _build_pdf(target, transactions, wallets, request, pdf_view):
    doc = SimpleDocTemplate(
        target,
        pagesize=portrait(LEDGER),
        leftMargin=50,
        rightMargin=50,
        topMargin=20,
        bottomMargin=20,
        title=f"{request.user.get_full_name()} Transaction Statement"
    )
    header_table, sub_header_table = pdf_view._build_corporate_header(wallets, request)
    elements = [
        header_table,
        sub_header_table,
        Spacer(1, 10),
        pdf_view._build_transactions_table(transactions, request),
        Spacer(1, 0),
        pdf_view._build_corporate_footer(),
    ]
    doc.build(
        elements,
        canvasmaker=lambda *args, **kwargs: NumberedCanvas(*args, pdf_view=pdf_view, **kwargs)
    )
