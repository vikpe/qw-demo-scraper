from dotenv import load_dotenv

from demo_scraper.scraper import ScrapeApp, ModeSettings


def main():
    load_dotenv()

    app = ScrapeApp(
        [
            ModeSettings("1on1", 250),
            ModeSettings("2on2", 50),
            ModeSettings("4on4", 200),
        ],
    )

    app.run_forever(
        add_interval=5,
        prune_interval=62,
    )


if __name__ == "__main__":
    main()
