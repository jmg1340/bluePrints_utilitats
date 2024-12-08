
class Config():
	SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
	#SQLALCHEMY_TRACK_MODIFICATIONS = False
	MONGO_URI="mongodb://localhost:27017/acces_portes"

class ProductionConfig(Config):
	#SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@prod_host:port/db_name'
	DEBUG = False


class DevelopmentConfig(Config):
	#SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@dev_host:port/db_name'
	DEBUG = True


class StagingConfig(Config):
	pass
	#SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@staging_host:port/db_name'

class TestingConfig(Config):
	DEBUG = True
	TESTING = True
	#SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@test_host:port/db_name'
