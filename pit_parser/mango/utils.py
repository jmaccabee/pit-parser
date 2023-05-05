import csv
import os

from django.conf import settings


def create_objects_from_source_file(source_filepath):
    with open(
        os.path.join(
            settings.MEDIA_ROOT,
            source_filepath,
        )
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        while reader:
            try:
                yield next(reader)
            except StopIteration:
                return
