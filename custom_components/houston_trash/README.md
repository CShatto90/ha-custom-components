# Houston Trash Integration

This integration provides sensors and calendars for Houston trash and recycling pickup schedules.

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