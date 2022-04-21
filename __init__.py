import configparser as conf
import pymysql


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


class stmq:
    '''
    Common functions for all things mq related
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

def baseConfig():
    '''
    Setup basic things we need for flask, including where the config file is

    Currently, all flask apps use the same appconfig and key so that authenication
    can be shard across different flask based services.
    '''

    configParser = conf.RawConfigParser()
    configFilePath = r'/etc/skatetrax/settings.conf'
    configParser.read(configFilePath)
    appConfig = configParser.get('appKey', 'secret')
    return appConfig


def dbconnect(sql, vTUP=None):
    '''
    Since all apps are using the same database settings, set them up here too
    '''

    configParser = conf.RawConfigParser()
    configFilePath = r'/etc/skatetrax/settings.conf'
    configParser.read(configFilePath)

    host = configParser.get('dbconf', 'host')
    user = configParser.get('dbconf', 'user')
    password = configParser.get('dbconf', 'password')
    db = configParser.get('dbconf', 'db')

    con = pymysql.connect(host=host, user=user, password=password,
                          db=db, cursorclass=pymysql.cursors.DictCursor,
                          autocommit=True)
    cur = con.cursor()
    cur.execute(sql, vTUP)
    tables = cur.fetchall()
    cur.connection.commit()
    con.close()
    return tables
