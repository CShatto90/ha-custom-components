# Houston Services for Home Assistant

This repository contains multiple custom components for Home Assistant that provide integration with various City of Houston services.

## Available Components

### Houston Incidents
Track active incidents in the Houston area with real-time updates.

### Houston Trash
Track regular trash and recycling collection schedules.

### Houston Heavy Trash
Track heavy trash and tree waste collection schedules.

## Installation

1. Install via HACS:
   - Add this repository as a custom repository in HACS
   - Choose "Integration" as the category
   - Click "Install"

2. Restart Home Assistant

3. Add the desired components to your configuration.yaml:

```yaml
# For Houston Incidents
sensor:
  - platform: houston_incidents
    name: "Houston Active Incidents"

# For Houston Trash
houston_trash:
  url: "https://api.recollect.net/api/areas/HoustonTX/services/1231/pages/en-US/place_calendar.json"

# For Houston Heavy Trash
houston_heavy_trash:
  routes:
    - name: "My Heavy Trash"
      route_id: "NE4TH_08"
```

4. Restart Home Assistant again to apply the configuration

See the individual component READMEs for more detailed configuration options. 