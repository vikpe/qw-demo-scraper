# QuakeWorld Demo Updater
> Downloads demos from QTVs, uploads to AWS S3 and stores info in database

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
