import configparser as conf

import os
import pymysql
from urllib.parse import quote_plus


class currencyUSD:
    '''
    Ensures that currency stuff is returned in a currency friendly format
    even if null, none, empty, etc
    '''

    def default(amount):
        if amount is None:
            return ("%0.2f" % float(0))
        else:
            return ("%0.2f" % float(amount))


class utils():
    '''
    Sometimes dividing to get hours from minutes leads to a weird result.
    This class fixes that so that it doesnt report 347.1666666667 hours
    but rather a 347 hours and nn minutes.
    '''

    def convertIceTime(m):
        h, m = divmod(m, 60)
        return {'hours': h, 'minutes': m}


class stmq:
    '''
    Common functions for all things mq related
    Not yet in use.
    '''

    def musicman():
        configParser = conf.RawConfigParser()
        configFilePath = r'/etc/skatetrax/settings.conf'
        configParser.read(configFilePath)
        musicmanSettings = {
        'host': configParser.get('stmq', 'hostname'),
        'user': configParser.get('stmq', 'username'),
        'password': configParser.get('stmq', 'password'),
        'queue': 'musicman'
        }

        return musicmanSettings


class db_handle():
    '''
    this class contains the basic building blocks for db queries
    '''

    def collect_credentials():
        '''
        first, collect all of the credentials
        '''

        username = os.environ['DB_USER']
        # password = quote_plus(os.environ['DB_PASS'])
        password = os.environ['DB_PASS']
        host = os.environ['DB_HOST']
        db = os.environ['DATABASE']

        creds = {'username': username,
                 'password': password,
                 'host': host,
                 'db': db
                 }
        return creds

    def dbconnect(sql, vTUP=None):
        '''
        Since all apps are using the same database settings, set them up here
        This function also recieves a sql query and returns the results
        '''
        c = db_handle.collect_credentials()
        con = pymysql.connect(host=c['host'], user=c['username'],
                              password=c['password'], db=c['db'],
                              cursorclass=pymysql.cursors.DictCursor,
                              autocommit=True)
        cur = con.cursor()
        cur.execute(sql, vTUP)
        tables = cur.fetchall()
        cur.connection.commit()
        con.close()
        return tables


def baseConfig():
    '''
    Setup basic things we need for flask, including where the config file is

    Currently, all flask apps use the same appconfig and key so that
    authentication can be shard across different flask based services.
    '''

    configParser = conf.RawConfigParser()
    configFilePath = r'/etc/skatetrax/settings.conf'
    configParser.read(configFilePath)
    appConfig = configParser.get('appKey', 'secret')
    return appConfig
