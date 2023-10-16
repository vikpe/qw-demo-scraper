# QuakeWorld Demo Scraper

> Downloads demos from QTVs, uploads to file storage and stores info in database

## Process

1. Check QTVs for recent demos
2. Compare to demos already in database
3. Upload demo to file storage
4. Parse and add info to database
5. Prune (delete) old demos

## Stack

* **File storage**: [AWS S3](https://aws.amazon.com/s3/)
* **Database**: [supabase](https://supabase.com/)
* **Languages**: python + shell script

## Rules

### Skipped demos

* game in progress
* already in database

### Ignored demos

* with bots
* where game is breaked/aborted
* with non-standard settings (dmm4 etc)
