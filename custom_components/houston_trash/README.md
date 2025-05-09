# Houston Trash Collection

This component integrates Houston trash collection schedule data into Home Assistant. It provides sensors and calendar entities for tracking trash collection schedules.

## Features
- Trash collection schedule tracking
- Calendar integration
- Next pickup date sensors

## Installation
1. Add this repository to HACS
2. Install the "Houston Trash" integration
3. Add configuration to your `configuration.yaml`

## Configuration
```yaml
houston_trash:
  scan_interval: 3600  # Optional, defaults to 1 hour
```

## Available Entities
- Calendar showing collection schedule
- Sensors for next pickup dates
- Binary sensors for collection day status

## Configuration

### Finding Your Recollect URL

1. Go to the [Houston Solid Waste Management website](https://www.houstontx.gov/solidwaste/)
2. Click on "Find Your Schedule" or use the search tool
3. Enter your address
4. Once your schedule loads, right-click and select "Inspect" (or press F12)
5. In the developer tools, go to the "Network" tab
6. Look for requests to `api.recollect.net`
7. Find a request that includes `place_calendar.json` in the URL
8. Copy the URL, but remove any `after` or `before` parameters
9. The URL should look like:
   ```
   https://api.recollect.net/api/areas/HoustonTX/services/1231/pages/en-US/place_calendar.json
   ```

### Example Configuration

```yaml
houston_trash:
  url: "https://api.recollect.net/api/areas/HoustonTX/services/1231/pages/en-US/place_calendar.json"
```

## Features

- Trash pickup sensor
- Recycling pickup sensor
- Trash pickup calendar
- Recycling pickup calendar

## Notes

- The integration will automatically handle the schedule updates
- Regular garbage collection is typically on schedule
- Recycling may be up to 2 days late
- Heavy trash collection is handled by a separate integration 