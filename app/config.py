from pydantic import BaseSettings


class ES_Settings(BaseSettings):
    host: str = "https://vpc-es-dev-log-z3dwk7x7qdkhozvhpvz7hpfgx4.ap-northeast-2.es.amazonaws.com"
    appuser: str = "esadmin"
    password: str = "Softwiz@12"


