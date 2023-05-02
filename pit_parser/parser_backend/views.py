import datetime
import re
import uuid

from django.shortcuts import redirect

from mango.models import MangoProductFile
from .models import ExtractedPitData

import pandas as pd


def process_data_file(request, mango_product_id, mango_product_file_id):
    data_file = MangoProductFile.objects.get(id=mango_product_file_id)
    if data_file.status == MangoProductFile.UNPROCESSED:
        data_file.status = MangoProductFile.PROCESSING
        data_file.save()

        # move this to a Celery queue?
        try:
            extracted_data_df = pd.read_csv(data_file.data_file)
            extracted_data_df["publication_date_str"] = extracted_data_df[
                "file_name"
            ].str.extract("(\\d{4}-\\d{2}-\\d{2})")
            extracted_data_df["publication_date"] = extracted_data_df[
                "publication_date_str"
            ].apply(lambda date_str: datetime.datetime.strptime(date_str, "%Y-%m-%d"))
            extracted_data_records = (
                ExtractedPitData(
                    mango_product_file=data_file,
                    raw_analysis_name=record.raw_analysis_name,
                    slice_value=record.slice_value,
                    section_header_1=record.section_header_1,
                    section_header_2=record.section_header_2,
                    source_sheet_name=record.file_tab_name,
                    source_data_file_name=record.file_name,
                    raw_date=record.date_header,
                    raw_value=record.value,
                    annotated=False,
                    timeseries_id=uuid.uuid3(
                        uuid.NAMESPACE_URL,
                        (
                            # remove slice_value and file_name from this line?
                            f"{record.raw_analysis_name}{record.slice_value}"
                            f"{record.section_header_1}{record.section_header_2}"
                            f"{record.file_tab_name}{record.file_name}"
                        ),
                    ),
                    publication_date=datetime.datetime.strptime(
                        re.search("(\\d{4}-\\d{2}-\\d{2})", record.date_header),
                        "%Y-%m-%d",
                    ).group(1),
                )
                for record in extracted_data_df.itertuples()
            )
            ExtractedPitData.objects.bulk_create(
                extracted_data_records,
                batch_size=10000,
            )
            data_file.status = MangoProductFile.PROCESSED
            data_file.save()
        except Exception:
            # rollback
            data_file.status = MangoProductFile.UNPROCESSED
            data_file.save()

    return redirect("view_product_data_files", id=mango_product_id)
