from django.urls import path
from .views import (
    CustomerImageView,
    QRCodeEncryptDataView,
    QRCodeDecryptDataView,
)


urlpatterns = [
    path('customer/images/<uuid:id>/<str:image_type>/', CustomerImageView.as_view(), name='customer-image-view'),

    # QR Code Encryption and Decryption
    path('qrcode/encrypt/', QRCodeEncryptDataView.as_view(), name='qrcode-encrypt'),
    path('qrcode/decrypt/', QRCodeDecryptDataView.as_view(), name='qrcode-decrypt'),
]
