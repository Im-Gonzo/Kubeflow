

class Config:

    def __init__(self) -> None:
        self.pipeline_func: None = None
        self.pipeline_template: None = None
        self.bucket: str = ''
        self.blob_name: str = ''
        self.local_file_path: str = ''
        self.display_name: str = ''
        self.template_path: str = f'gs://{self.bucket}'
        self.pipeline_root: str = ''
        self.caching: bool = False
        self.project_name: str = ''
        self.location: str = ''
        self.labels: dict = {}
        self.params: dict = {}
        self.service_account: str = ''