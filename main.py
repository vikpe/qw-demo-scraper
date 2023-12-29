from dotenv import load_dotenv

from demo_scraper.scraper import ScrapeApp, ModeSettings


def main():
    load_dotenv()

    app = ScrapeApp(
        [
            ModeSettings("1on1", 800),
            ModeSettings("2on2", 300),
            ModeSettings("4on4", 4800),
            ModeSettings("ctf", 800),
        ],
    )

    app.run_forever(
        add_interval=5,
        prune_interval=62,
    )


if __name__ == "__main__":
    main()
