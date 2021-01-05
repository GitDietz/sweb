from io import BytesIO
from django.core.files import File
from django.db import models

from PIL import Image, ImageDraw
import qrcode


class QR(models.Model):
    """
    """
    name = models.CharField(max_length=200, blank=False, null=False)
    url = models.URLField()
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.name)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
        # to make it better, create the code from the url not the name
