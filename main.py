from dotenv import load_dotenv

from demo_scraper.scraper import ScrapeApp, ModeSettings


def main():
    load_dotenv()

    app = ScrapeApp(
        [
            ModeSettings("1on1", 1000),
            ModeSettings("2on2", 600),
            ModeSettings("4on4", 4800),
            ModeSettings("ctf", 800),
            ModeSettings("wipeout", 75),
        ],
    )

    app.run_forever(
        add_interval=5,
        prune_interval=62,
    )


if __name__ == "__main__":
    main()
