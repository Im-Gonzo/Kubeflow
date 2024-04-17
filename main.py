import logging
from config import Config
from google.cloud import storage
from google.cloud import aiplatform
from kfp.compiler import Compiler


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class Pipeline:

    def __init__(self, config: Config = Config()) -> None:
        self.config = config
        self.compiler = Compiler()
    

    def submit_job(self) -> None:
        """Submits the pipeline job into Vertex AI"""
        job = aiplatform.PipelineJob(
            display_name=self.config.display_name,
            template_path=self.config.template_path,
            pipeline_root=self.config.pipeline_root,
            enable_caching=self.config.caching,
            project=self.config.project_name,
            location=self.config.location,
            labels=self.config.labels,
            parameter_values=self.config.params,
        )

        try:
            logging.info('Submitting job')
            job.submit(service_account=self.config.service_account)
            logging.info('Job submitted successfully')
        except Exception as e:
            logging.error('Failed to submit job')
            logging.error(e)

    def compile_job(self) -> None:
        """Compiles the Kubeflow Pipeline function into a manifest for deployment."""
        try:
            logging.info(f'Starting pipeline compilation')
            self.compiler.compile(pipeline_func=self.config.pipeline_func, package_path=self.config.pipeline_template)
            logging.info('Compilation completed.')
        except Exception as e:
            logging.error(e)

    def upload_template_to_gcs(self) -> None:
        """Saves the Kubeflow pipeline tempalte into GCS"""
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name=self.config.bucket)
        blob = bucket.blob(blob_name=self.config.blob_name)

        try:
            logging.info(f'Saving template to GCS')
            blob.upload_from_filename(filename=self.config.local_file_path, num_retries=3)
            logging.info('Template saved to GCS')
        except Exception as e:
            logging.error('Failed to save tempalte to GCS')
            logging.error(e)


if __name__ == "__main__":

    pipeline = Pipeline()

    pipeline.compile_job()

    pipeline.upload_template_to_gcs()

    pipeline.submit_job()