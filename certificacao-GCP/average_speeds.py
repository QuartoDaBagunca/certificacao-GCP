# from src.beam_bigquery import BeamBigquery
import apache_beam as beam
import os
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions, SetupOptions

topic_id = f'projects/{os.environ["DEVSHELL_PROJECT_ID"]}/topics/{os.environ["TOPIC_NAME"]}'
    
# beamBq = BeamBigquery('streaming')

#Parâmetros da tabela modelo do BQ (obter schema)
dataset_name = 'demos'
table_name = 'average_speeds_agg_new'

structury = {
    "average_speeds_fields": {
        "fields": [
            {"name": "timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"}, 
            {"name": "latitude", "type": "FLOAT", "mode": "NULLABLE"}, 
            {"name": "longitude", "type": "FLOAT", "mode": "NULLABLE"}, 
            {"name": "highway", "type": "STRING", "mode": "NULLABLE"}, 
            {"name": "direction", "type": "STRING", "mode": "NULLABLE"}, 
            {"name": "lane", "type": "INTEGER", "mode": "NULLABLE"}, 
            {"name": "speed", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "sensorId", "type": "STRING", "mode": "NULLABLE"}
        ]
    },
    "average_speeds_agg_fields": {
        "fields": [
            {"name": "sensorId", "type": "STRING", "mode": "NULLABLE"},
            {"name": "speed", "type": "FLOAT", "mode": "NULLABLE"}
        ]
    }
}

table_schema = structury['{}_fields'.format(table_name)]
schema = table_schema['fields']
# Obter o esquema da tabela
# table_schema, schema = beamBq.get_schema(table_name, dataset_name)

# class AverageSpeeds(beam.DoFn):

#     """
#     Return data in adherent format to insert beam->bigquery
#     """

#     def dict_builder(self, record:list, schema:list) -> dict:

#         dict_ = {} 

#         for row in range(len(schema)):
#             dict_[schema[row]['name']] = record[row]

#         return(dict_)

def dict_builder(record:list, schema:list) -> dict:

    dict_ = {} 

    for row in range(len(schema)):
        dict_[schema[row]['name']] = record[row]

    return(dict_)

def run():

    options = PipelineOptions()
    gcp_options = options.view_as(GoogleCloudOptions)
    gcp_options.view_as(SetupOptions).save_main_session = True
    gcp_options.view_as(StandardOptions).streaming = True
    gcp_options.project = os.environ['DEVSHELL_PROJECT_ID']
    gcp_options.job_name = 'average-speeds'
    gcp_options.staging_location = f'gs://{os.environ["BUCKET"]}/staging'
    gcp_options.temp_location = f'gs://{os.environ["BUCKET"]}/temp'
    gcp_options.region = os.environ['REGION']
    table_spec = f'{gcp_options.project}.{dataset_name}.{table_name}'

    # Definir o runner como DataflowRunner
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    
    # Criar o pipeline
    with beam.Pipeline(options=gcp_options) as p:
        (p
         | 'Read from PubSub' >> beam.io.ReadFromPubSub(topic=topic_id)
         | 'Parse PubSub Message' >> beam.Map(lambda record: (record[7], float(record[6])))
         | 'Apply Window' >> beam.WindowInto(beam.window.FixedWindows(60))  # Window 60 sec
         | 'Sum p/ key' >> beam.CombinePerKey(sum)
         | 'Format data to BigQuery' >>  beam.Map(lambda record: dict_builder(record, schema)) 
         | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                table_spec,
                schema=table_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )
        )

if __name__ == '__main__':
    run()

    # Validando schema gerado
    # print(f"schema type {type(table_schema)} \n schema structury: {table_schema}")