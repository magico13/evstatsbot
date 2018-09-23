# evstatsbot
A reddit bot that gives stats on the electric vehicles mentioned in a submission

## Why does this exist?
This bot was made to serve as a quick reference for EVs that are mentioned in a thread. For an enthusiast this is probably not that helpful, but for a newcomer who doesn't know the difference between a LEAF and a Kona, or a Volt and a Bolt it provides some initial info without having to search for it.

## Want to provide info on a vehicle?
Just submit an issue or pull request with the information formatted as follows. Only provide duplicates where range or performance is noticeably different (like LEAF gen 1 having 24kwh and 30kwh batteries, or the i3 with 22kwh and 33kwh), not for other packages (premium interior, automation features, etc).

```
{
  "id": "unique_id",
  "search_regex": [
  "\\bname1\\b",
  "\\bname2\\b" #etc, like "Model S" or "P85D" both may refer to a Tesla Model S
  ],
  "title": "Manufacturer CarName",
  "type": "BEV/PHEV",
  "ev_range": 00, #EPA rated miles
  "battery_size": 00, #Battery size in kwh
  "zero_sixty": 1.2, #0 to 60 in seconds
  "msrp": 13370, #MSRP in US dollars, preferably at launch and for base trim
  "year_start": 2099, #First model year
  "year_end": 2100, #Last model year, remove if still in production
  "qc_type": "None/CCS/CHAdeMO/Tesla" #Add an * if it's an optional package (like Bolt, LEAF)
}
```

## Known vehicles still needing added
- Toyota Prius Prime
- Toyota Prius Plug-in
