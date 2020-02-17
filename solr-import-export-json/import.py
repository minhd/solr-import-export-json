import json
import logging.config
import os
from itertools import islice

import click
import urllib3

logger = logging.getLogger()


@click.command()
@click.option("--solr_url", "-s", help="SOLR URL", prompt=True)
@click.option("--file_path", "-f", help="Output File Path", prompt=True)
@click.option("--rows", "-r", default=5000, help="Number of rows per batch")
@click.option("--debug/--no-debug", "-d", default=False, help="Debug")
def solr_import(solr_url, file_path, rows, debug):
    """
    Import to a solr collection from a file
    """
    if debug:
        logger.setLevel(logging.DEBUG)

    update_url = solr_url + "/update"
    logger.info("Importing {} to {}".format(file_path, update_url))

    http = urllib3.PoolManager()
    sofar = 0
    total = file_len(file_path)
    logger.debug("Total: {}".format(total))

    with open(file_path, "rb") as f:
        for n_lines in iter(lambda: tuple(islice(f, rows)), ()):
            logger.debug("Processing: {}".format(len(n_lines)))
            docs = []
            for line in n_lines:
                line = json.loads(line.decode("utf-8"))
                del line["_version_"]
                docs.append(line)
            # logger.debug(json.dumps(docs, indent=2))

            logger.debug("Adding {} documents to {}".format(len(docs), update_url))
            r = http.request(
                "POST",
                update_url,
                body=json.dumps(docs),
                headers={"Content-Type": "application/json"},
            )
            result = json.loads(r.data.decode("utf-8"))
            logger.debug(json.dumps(result))
            if result["responseHeader"]["status"] != 0:
                logger.error(result["error"]["msg"])
            sofar += len(docs)
            logger.info("Processed: {}/{}".format(sofar, total))

    logger.debug("Committing")
    r = http.request("GET", update_url + "?commit=true")
    result = json.loads(r.data.decode("utf-8"))
    logger.debug(json.dumps(result))

    logger.info("Finished")


# pylint: disable=unused-variable
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(ROOT_DIR, "logging.conf")
    logging.config.fileConfig(CONFIG_PATH)
    solr_import()
