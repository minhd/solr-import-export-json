import fnmatch
import json
import logging
from logging import config
import os
import re
import sys
from pprint import pprint
from urllib.parse import urlencode
import click
import urllib3

logger = logging.getLogger()


@click.command()
@click.option('--solr_url', '-s', help='SOLR URL', prompt=True)
@click.option('--file_path', '-f', help='Output File Path', prompt=True)
@click.option('--rows', '-r', default=5000, help="Number of rows per batch")
@click.option('--exclude_pattern', '-e', default=False, help="Exclude")
@click.option('--debug/--no-debug', '-d', default=False, help="Debug")
def solr_export(solr_url, file_path, rows, exclude_pattern, debug):
    """
    Export solr collection to a file
    """
    if debug:
        logger.setLevel(logging.DEBUG)

    #logger.debug("Deleting %s", file_path)
    #os.remove(file_path)

    logger.debug("Opening %s for writing", file_path)
    f = open(file_path, "w+")

    http = urllib3.PoolManager()
    cursor = "*"
    sort = 'id asc'
    pattern = exclude_pattern

    logger.info("SOLR URL %s", solr_url)
    logger.info("File path: %s", file_path)
    if pattern:
        logger.info("Exclude pattern: %s", pattern)
    # pprint(params, width=1)

    finished = False
    sofar = 0
    while not finished:
        params = {
            'q': '*:*',
            'sort': sort,
            'rows': rows,
            'start': 0,
            'cursorMark': cursor
        }
        url = prep_url(solr_url, params)
        result = get_url(url, http)
        docs = result['response']['docs']
        total = result['response']['numFound']
        next_cursor = result['nextCursorMark']
        logger.debug("cursor: %s, next: %s", cursor, next_cursor)
        for doc in docs:
            doc = exclude(doc, pattern)
            f.write(json.dumps(doc))
            f.write(os.linesep)
        sofar += len(docs)
        logger.info("Written %s/%s", sofar, total)
        if cursor == next_cursor:
            finished = True
        else:
            cursor = next_cursor
        logger.debug("next cursor: %s", cursor)
    logger.info("Finished")
    f.close()


def prep_url(solr_url, params):
    query_string = urlencode(params)
    logger.debug('params: %s', query_string)
    url = solr_url + '/select?' + query_string
    logger.debug("url: %s", url)
    return url


def get_url(url, http):
    logger.debug("getting url: %s", url)
    r = http.request('GET', url)
    logger.debug("status: %s", r.status)
    result = json.loads(r.data.decode('utf-8'))
    return result


def exclude(doc, pattern):
    if not pattern:
        return doc
    remove = list(filter(lambda x: match(x, pattern), list(doc.keys())))
    for key in remove:
        del doc[key]
    return doc


def dd(thing=None):
    if thing:
        pprint(thing)
    sys.exit()


def match(string, pattern):
    patterns = pattern.split(",")
    for x in patterns:
        p = fnmatch.translate(x)
        if re.compile(p).match(string):
            return True
    return False

# pylint: disable=no-value-for-parameter
if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(ROOT_DIR, 'logging.conf')
    logging.config.fileConfig(CONFIG_PATH)
    solr_export()
