# QuakeWorld Demo Scraper
> Downloads demos from QTVs, uploads to file storage and stores parsed info in database

## Process
1. Check QTVs for demos
2. Compare to demos already in database
4. Upload demo to file storage
5. Parse info
6. Add info to database
7. Prune old demos

## TODO
* [x] Download recent demos
  * [x] 1on1
  * [x] 2on2
  * [x] 4on4
  * [ ] CTF
* [x] Parse info
  * [x] Mode, map, players/teams, duration
  * [x] Checksum (sha256)
* [x] Store file in file storage (AWS S3)
* [x] Store info in database (supabase)
* [x] Prune old demos
* [x] Strip prefixes/suffixes from player names
* [x] Skip demos
  * [x] game in progress
  * [x] already in database
* [x] Ignore demos
  * [ ] with bots
  * [x] where game is breaked/aborted
  * [ ] with non-standard settings (dmm4 etc)
