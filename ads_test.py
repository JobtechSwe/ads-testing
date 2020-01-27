import logging
import sys

import psycopg2

import queries
import settings
from flask import Flask
from flask import jsonify

from utils import Advertisements

app = Flask(__name__)
log = logging.getLogger(__name__)


if settings.PG_DBNAME and settings.PG_USER:
    try:
        if not settings.PG_HOST:
            log.info("PG_HOST not set, assuming local socket")
            pg_conn = psycopg2.connect(dbname=settings.PG_DBNAME,
                                       user=settings.PG_USER)
        else:
            pg_conn = psycopg2.connect(host=settings.PG_HOST,
                                       port=settings.PG_PORT,
                                       dbname=settings.PG_DBNAME,
                                       user=settings.PG_USER,
                                       password=settings.PG_PASSWORD,
                                       sslmode=settings.PG_SSLMODE)
    except psycopg2.OperationalError as e:
        log.error("Failed to connect to PostgreSQL on %s:%s" % (settings.PG_HOST,
                                                                settings.PG_PORT))
        log.error("Reason for PostgreSQL failure: %s" % str(e))
        sys.exit(1)


@app.route('/sokningar/publiceradeannonser')
def fetch_ads():
    ads_list = ('23511466', '8461698', '8467834', '8467833')
    cur = pg_conn.cursor()
    cur.execute(queries.ADS_QUERY, [ads_list])
    result = {"idLista": [item[0] for item in cur.fetchall()]}
    cur.close()

    return jsonify(result)


@app.route('/annonser/<annonsId>')
def search_ad(annonsId):
    cur = pg_conn.cursor()
    cur.execute(queries.AD_ANNONSTEXT_QUERY, [annonsId])

    #fetch ads and mock them
    text = cur.fetchone()
    mocked_text = Advertisements(text[0]).mask_sensitive_info()
    mocked_formaterad_text = Advertisements(text[1]).mask_sensitive_info()

    cur.execute(queries.AD_ALL_QUERY, [annonsId])
    result = cur.fetchone()[0]

    result['annonstext'] = mocked_text
    result['annonstextFormaterad'] = mocked_formaterad_text

    cur.close()
    return jsonify(result)
