from pydantic import BaseSettings


class ES_Settings(BaseSettings):
    host: str = "https://es_id.region.es.amazonaws.com"
    appuser: str = "userid"
    password: str = "password"


