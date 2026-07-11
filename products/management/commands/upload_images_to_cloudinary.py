import os
from django.core.management.base import BaseCommand
from django.core.files import File
from products.models import Product


class Command(BaseCommand):
    help = 'Re-upload all product images from local media/ to Cloudinary storage'

    def handle(self, *args, **options):
        products = Product.objects.exclude(image='').exclude(image=None)
        total = products.count()

        if total == 0:
            self.stdout.write(self.style.WARNING('No products with images found.'))
            return

        self.stdout.write(f'Found {total} products with images. Starting upload...\n')
        success = 0
        failed = 0

        for product in products:
            try:
                image_path = product.image.path
            except Exception:
                self.stdout.write(
                    self.style.WARNING(f'  [{product.name}] Cannot get local path (already on cloud?)')
                )
                failed += 1
                continue

            if not os.path.exists(image_path):
                self.stdout.write(
                    self.style.WARNING(f'  [{product.name}] Local file not found: {image_path}')
                )
                failed += 1
                continue

            try:
                filename = os.path.basename(image_path)
                with open(image_path, 'rb') as f:
                    product.image.save(filename, File(f), save=True)

                self.stdout.write(
                    self.style.SUCCESS(f'  Uploaded: {product.name} -> {product.image.url}')
                )
                success += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  Failed: {product.name} - {e}')
                )
                failed += 1

        self.stdout.write(f'\nDone! {success} uploaded, {failed} failed.')
