from crawler_kit.modules.pchome.application.commands.crawl_pchome_web import (
    PchomeWebCrawler,
)
from shortuuid import uuid
from os import environ


def handle_crawl_pchome_web(url: str, request_delay: int = 1, dev: bool = False):
    trace_id = uuid()
    if not dev:
        environ.setdefault("HEADLESS", "True")
    handler = PchomeWebCrawler(request_delay, trace_id)
    flow = handler.__call__.with_options(flow_run_name=trace_id)
    return flow(url)
