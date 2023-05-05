/* useful for testing different strategies for deriving a timeseries_id */
WITH ts_new AS (
    SELECT DISTINCT raw_analysis_name||slice_value||section_header_1||section_header_2||source_sheet_name AS timeseries_id_new
    FROM parser_backend_extractedpitdata OFFSET 1 LIMIT 1
),
extraction AS (
    SELECT 
        *, raw_analysis_name||slice_value||section_header_1||section_header_2||source_sheet_name AS timeseries_id_new
    FROM parser_backend_extractedpitdata
),
sample AS (
    SELECT 
        raw_analysis_name,
        slice_value, 
        section_header_1,
        section_header_2,
        source_sheet_name,
        raw_date,
        raw_value,
        sent_date
        --,ROW_NUMBER() OVER (
        --    PARTITION BY e.timeseries_id_new --, slice_value 
        --    ORDER BY sent_date DESC, raw_date DESC
        --) AS sample_number
    FROM extraction AS e
    JOIN mango_yipitreportcampaigndatafile AS y
    ON y.id = e.source_data_file_name
    JOIN ts_new USING (timeseries_id_new)
)
SELECT * FROM sample LIMIT 50; --WHERE sample_number < 6;