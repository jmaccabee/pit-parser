import uuid

from django.shortcuts import render

from mango.models import MangoProductFile
from .models import ExtractedPitData

import pandas as pd


def process_data_file(request, mango_product_id, mango_product_file_id):
    data_file = MangoProductFile.objects.get(id=mango_product_file_id)
    extracted_data_df = pd.read_csv(data_file.data_file)
    extracted_data_records = (
        ExtractedPitData(
            mango_product_file=data_file,
            raw_analysis_name=record.raw_analysis_name,
            slice_value=record.slice_value,
            section_header_1=record.section_header_1,
            section_header_2=record.section_header_2,
            source_sheet_name=record.file_tab_name,
            source_data_file_name=record.file_name,
            date=record.date_header,
            value=record.value,
            timeseries_id=uuid.uuid3(
                uuid.NAMESPACE_URL,
                (
                    f"{record.raw_analysis_name}{record.slice_value}"
                    f"{record.section_header_1}{record.section_header_2}"
                ),
            ),
        )
        for record in extracted_data_df.itertuples()
    )
    ExtractedPitData.objects.bulk_create(
        extracted_data_records,
        batch_size=10000,
    )
