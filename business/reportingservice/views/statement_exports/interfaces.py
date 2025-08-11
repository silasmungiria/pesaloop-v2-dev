# Standard library imports
from datetime import datetime, timedelta

# Third-party library imports
from django.db import models
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER

# Project-specific imports
from userservice.models import Customer
from reportingservice.utils import (
  APP_NAME,
  APP_VERSION,
  EMAIL_REPLY_TO,
  COPYRIGHT_YEAR,
  FRONTEND_PRODUCTION_URL
)


class BasePDFContentBuilder:
    """Base class with common PDF report utilities."""

    def _header_style(self, font_size=12, bold=False):
        return ParagraphStyle(
            name="HeaderStyle",
            fontSize=font_size,
            fontName="Helvetica-Bold" if bold else "Helvetica",
            alignment=0,
            spaceAfter=10,
        )


    def _table_text_style(self, font_size=9):
        return ParagraphStyle(
            name="TableTextStyle",
            fontSize=font_size,
            fontName="Helvetica",
            leading=12,
        )


    def _build_corporate_header(self, wallet, request):
        """Creates a polished corporate header with separated main and sub header."""
        company_name = f"{APP_NAME} Financial Services"
        statement_title = "TRANSACTION STATEMENT"
        period_start = (datetime.now() - timedelta(days=180)).strftime("%d %b %Y")
        period_end = datetime.now().strftime("%d %b %Y")
        wallet_count = wallet.count() if isinstance(wallet, models.QuerySet) else 1

        # Opening balance for each wallet
        if isinstance(wallet, models.QuerySet):
            current_balances = [f"{w.currency} {w.balance:,.2f}" for w in wallet]
            current_balance_str = ", ".join(current_balances)
        else:
            current_balance_str = f"{wallet.currency} {wallet.balance:,.2f}"

        user = request.user
        user_customer = Customer.objects.filter(user=user).first()
        user_address = self._format_user_address(user_customer) if user_customer else "Not Provided"

        # Styles
        styles = {
            "company": ParagraphStyle(
                name="CompanyStyle",
                fontName="Helvetica-Bold",
                fontSize=16,
                textColor=colors.HexColor("#002244"),
                alignment=TA_CENTER,
                spaceAfter=8
            ),
            "title": ParagraphStyle(
                name="TitleStyle",
                fontName="Helvetica-Bold",
                fontSize=12,
                textColor=colors.HexColor("#005B9F"),
                alignment=TA_CENTER,
                spaceAfter=10,
                leading=14
            ),
            "value": ParagraphStyle(
                name="ValueStyle",
                fontName="Helvetica",
                fontSize=9,
                textColor=colors.HexColor("#555555"),
                leading=12
            ),
        }

        # Main header content
        main_content = [
            Paragraph(company_name, styles["company"]),
            Paragraph(statement_title, styles["title"]),
        ]

        header_table = Table([[main_content]], colWidths=["100%"], hAlign="CENTER")
        header_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("TOPPADDING", (0, 0), (-1, -1), 20),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
            ("LINEBELOW", (0, 0), (-1, -1), 1, colors.HexColor("#F8FAFC")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))

        # Sub-header content
        left_content = [
            Paragraph(f"<b>Name:</b> {user.get_full_name()}", styles["value"]),
            Spacer(1, 6),
            Paragraph(f"<b>Account No.:</b> {user.account_number}", styles["value"]),
            Spacer(1, 6),
            Paragraph(f"<b>Email Address:</b> {user.email}", styles["value"]),
            Spacer(1, 6),
            Paragraph(f"<b>Mobile Number:</b> {getattr(user, 'phone_number', 'N/A')}", styles["value"]),
            Spacer(1, 6),
            Paragraph(f"<b>Statement Period:</b> {period_start} to {period_end}", styles["value"]),
            Spacer(1, 10),
        ]

        right_content = [
            Paragraph(f"<b>Generated On:</b> {datetime.now().strftime('%d %b %Y %H:%M:%S')}", styles["value"]),
            Spacer(1, 6),
            Paragraph(f"<b>Mailing Address:</b> {user_address}", styles["value"]),
            Spacer(1, 6),
            Paragraph(f"<b>Linked Wallets:</b> {wallet_count} {'wallet' if wallet_count == 1 else 'wallets'}", styles["value"]),
            Spacer(1, 6),
            Paragraph(f"<b>Current Balance:</b> {current_balance_str}", styles["value"]),
            Spacer(1, 6),
            Spacer(1, 10),
        ]

        sub_header_table = Table(
            [[left_content, right_content]],
            colWidths=["50%", "50%"],
            hAlign="LEFT"
        )
        sub_header_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("LEFTPADDING", (0, 0), (0, 0), 0),
            ("LEFTPADDING", (1, 0), (1, 0), 0),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEBELOW", (0, 0), (-1, -1), 1, colors.HexColor("#F8FAFC")),
        ]))


        return header_table, sub_header_table


    def _format_user_address(self, customer_data):
        """Formats Customer address into a readable string."""
        address_parts = [
            customer_data.address or customer_data.postal_address or "",
            customer_data.postal_code or "",
            customer_data.city or "",
            customer_data.country or ""
        ]
        return ", ".join(filter(None, address_parts)).strip()


    def _build_transactions_table(self, transactions, request):
        """Create a styled transactions table."""
        headers = ["Date", "Description", "Status", "Amount Out", "Amount In"]
        data = [headers]

        for transaction in transactions:
            if transaction.sender_wallet.wallet_owner == request.user:
                currency_symbol = transaction.currency
                money_out, money_in = transaction.amount, 0
                details = f"Sent to {transaction.receiver_wallet.wallet_owner.get_full_name()} (Ref: {transaction.reference_id})"
            else:
                currency_symbol = transaction.currency
                money_out, money_in = 0, transaction.amount
                details = f"Received from {transaction.sender_wallet.wallet_owner.get_full_name()} (Ref: {transaction.reference_id})"

            data.append([
                transaction.created_at.strftime("%d-%m-%Y %H:%M:%S"),
                Paragraph(details, self._table_text_style(font_size=9)),
                transaction.status.replace("_", " ").title(),
                f"{currency_symbol} {money_out:,.2f}" if money_out else "",
                f"{currency_symbol} {money_in:,.2f}" if money_in else "",
            ])

        table = Table(data, colWidths=[110, 240, 100, 140, 140])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, 0), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 11),
            ("TOPPADDING", (0, 0), (-1, 0), 15),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 15),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ("ALIGN", (2, 1), (2, -1), "LEFT"),
            ("ALIGN", (0, 1), (1, -1), "LEFT"),
            ("ALIGN", (3, 1), (4, -1), "RIGHT"),
            ("LEFTPADDING", (3, 1), (4, -1), 20),
            ("RIGHTPADDING", (3, 1), (4, -1), 20),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("TOPPADDING", (0, 1), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 12),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ]))
        return table


    def _build_corporate_footer(self):
        footer_text = (
            f"{APP_NAME} Financial Services\n"
            f"Website: {FRONTEND_PRODUCTION_URL}\n"
            f"Contact: {EMAIL_REPLY_TO}\n"
            f"Version: {APP_VERSION}\n"
            f"© {COPYRIGHT_YEAR} All rights reserved."
        )

        return Paragraph(
            footer_text,
            ParagraphStyle(
                name="FooterStyle",
                fontSize=8,
                fontName="Helvetica",
                alignment=1,
                textColor=colors.grey,
                spaceBefore=20,
                spaceAfter=10,
            ),
        )


    def _add_page_number(self, canvas, doc=None, total_pages="?"):
        page_num = canvas.getPageNumber()
        text = f"Page {page_num} of {total_pages}"
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(770, 10, text)


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, pdf_view=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.pdf_view = pdf_view

    def showPage(self):
        """Save the current page state and start a new page."""
        self._saved_page_states.append(dict(self.__dict__))  # save state
        self._startPage()

    def save(self):
        """Draw page numbers and save each page once."""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self.pdf_view:
                self.pdf_view._add_page_number(self, doc=None, total_pages=num_pages)
            super().showPage()  # create final page
        super().save()
