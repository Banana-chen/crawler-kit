from typer import Typer
from crawler_kit.modules.pchome.presentation.cli.handlers.handle_crawl_pchome_web import (
    handle_crawl_pchome_web,
)

crawlers = Typer(name="pchome", help="Pchome crawler")
crawlers.command(name="web", help="crawl Pchome web content by url")(
    handle_crawl_pchome_web
)
