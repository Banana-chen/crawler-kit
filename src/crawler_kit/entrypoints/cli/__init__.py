import atexit
from typer import Typer
from click.core import Context
from crawler_kit.utils.asyncio import ensure_event_loop
from crawler_kit.utils.lifespans.startup import startup, shutdown
from crawler_kit.entrypoints.cli.pchome import crawlers as pchome_crawlers
from crawler_kit.entrypoints.cli.ebay import crawlers as ebay_crawlers
from crawler_kit.entrypoints.cli.lazada import crawlers as lazada_crawlers
from crawler_kit.entrypoints.cli.amazon import crawlers as amazon_crawlers


def setup_async(context: Context):
    loop = ensure_event_loop()
    context.obj = loop.run_until_complete(startup())
    atexit.register(lambda: loop.run_until_complete(shutdown()))


typer = Typer(callback=setup_async)
typer.add_typer(pchome_crawlers)
typer.add_typer(ebay_crawlers)
typer.add_typer(lazada_crawlers)
typer.add_typer(amazon_crawlers)
