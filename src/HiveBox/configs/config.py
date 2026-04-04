# Config.py

'''Configuration classes for HiveBox application'''


class Config:
    """Base configuration class with default settings"""

    app_name = "HiveBox"
    version = "1.0.0"
    debug = True
    database_uri = "sqlite:///hivebox.db"
    api_prefix = "/api/v1"
    allow_hosts = ["localhost", "0.0.0.0"]
    log_level = "DEBUG"
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file = "hivebox.log"


class DevelopmentConfig(Config):
    """Development configuration with debug settings"""
    debug = True
    database_uri = "sqlite:///hivebox_dev.db"


class ProductionConfig(Config):
    """Production configuration with optimized settings"""

    debug = False
    database_uri = "postgresql://user:password@localhost/hivebox_prod"


class TestingConfig(Config):
    """Testing configuration with test settings"""

    debug = True
    database_uri = "sqlite:///hivebox_test.db"
