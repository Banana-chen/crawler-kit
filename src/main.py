if __name__ == "__main__":
    from dotenv import load_dotenv
    from os.path import exists
    from os import environ

    environ["RUN_MODE"] = "cli"
    for env_file in ["src/.env", "src/.env.local"]:
        if exists(env_file):
            load_dotenv(env_file, override=True)

    from crawler_kit.entrypoints.cli import typer

    typer()
else:
    from crawler_kit.entrypoints.http.admin import admin  # noqa: F401
    from crawler_kit.entrypoints.pubsub.on_crawling_ebay import *  # noqa: F403
    from crawler_kit.entrypoints.pubsub.on_crawling_amazon import *  # noqa: F403
    from crawler_kit.entrypoints.pubsub.on_crawling_lazada import *  # noqa: F403
    from crawler_kit.entrypoints.pubsub.on_crawling_pchome import *  # noqa: F403
