_ENVIRONMENTS = {

                 'DEV': {
                                'environment': 'DEVELOPMENT',
                                'redis_host': 'localhost',
                                'redis_port': 6379,

                            },
                    ## other environments data goes here
                }

APP_ENV = 'DEV' #mocked ENV Variable

environment = _ENVIRONMENTS[APP_ENV]['environment']
redis_host = _ENVIRONMENTS[APP_ENV]['redis_host']
redis_port = _ENVIRONMENTS[APP_ENV]['redis_port']


