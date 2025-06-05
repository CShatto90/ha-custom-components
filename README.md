# Houston Services for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant integration that provides Houston city services monitoring through a unified interface. Monitor trash collection, heavy trash schedules, and active incidents all from one integration.

## Features

### 🗑️ Regular Trash & Recycling
- Track regular trash and recycling pickup schedules
- Calendar integration for upcoming pickups
- Pickup status and delay notifications
- Zone-based information

### 🚛 Heavy Trash Collection
- Monitor heavy trash collection progress for your route
- Real-time status updates (In Progress, Scheduled, Completed)
- Service week and day information
- ArcGIS-powered data

### 🚨 Active Incidents
- Monitor active Fire Department and Police incidents
- Real-time incident counts
- Incident details and locations

## Installation

### HACS (Recommended)
1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click "Explore & Download Repositories"
4. Search for "Houston Services"
5. Download and restart Home Assistant

### Manual Installation
1. Download the latest release from GitHub
2. Copy `custom_components/houston_services` to your `<config>/custom_components/` directory
3. Restart Home Assistant

## Configuration

### Initial Setup
1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"Houston Services"**
4. Select which services you want to enable:
   - **Regular Trash & Recycling**: Track regular waste collection schedules
   - **Heavy Trash**: Monitor heavy trash collection progress
   - **Active Incidents**: Monitor emergency incidents

### Service Configuration

#### Regular Trash & Recycling
- **API Base URL**: The Recollect API endpoint for Houston trash data
- Default URL is provided, but you may need to adjust for your specific area

#### Heavy Trash
- **Route Name**: A friendly name for your heavy trash route
- **Route ID**: Your heavy trash route identifier (e.g., `SW4TH_08`)

To find your route ID:
1. Visit the [Heavy Trash Progress Dashboard](https://mycity.maps.arcgis.com/apps/dashboards/cb0ac86b3b434513b5f22428385820f3)
2. Search for your address or zoom to your location
3. Click on your area to see route information
4. The route ID format: `[QUADRANT][WEEK][DAY]_[NUMBER]`
   - `SW4TH_08` = Southwest, 4th week, Thursday, route 08

#### Active Incidents
- No additional configuration required
- Automatically monitors citywide incidents

## Entities Created

### Regular Trash & Recycling
- `sensor.houston_trash_next_pickup` - Next trash pickup date
- `sensor.houston_recycling_next_pickup` - Next recycling pickup date
- `calendar.houston_trash_pickup_calendar` - Trash pickup calendar
- `calendar.houston_recycling_pickup_calendar` - Recycling pickup calendar

### Heavy Trash
- `sensor.[route_name]_status` - Current collection status
- `sensor.[route_name]_next_pickup` - Next pickup date
- `sensor.[route_name]_service_type` - Type of service
- `sensor.[route_name]_service_week` - Service week
- `sensor.[route_name]_service_day` - Service day
- `sensor.[route_name]_quadrant` - Area quadrant
- `calendar.[route_name]_calendar` - Heavy trash calendar

### Active Incidents
- `sensor.houston_active_incidents` - Total active incidents count

## Automation Examples

### Trash Day Reminder
```yaml
automation:
  - alias: "Trash Day Reminder"
    trigger:
      - platform: time
        at: "18:00:00"
    condition:
      - condition: template
        value_template: >
          {{ as_timestamp(states('sensor.houston_trash_next_pickup')) - as_timestamp(now()) <= 86400 }}
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "Don't forget to put out the trash! Pickup is tomorrow."
```

### Heavy Trash Status Update
```yaml
automation:
  - alias: "Heavy Trash Status Update"
    trigger:
      - platform: state
        entity_id: sensor.my_heavy_trash_route_status
    action:
      - service: notify.family
        data:
          message: "Heavy trash status updated: {{ states('sensor.my_heavy_trash_route_status') }}"
```

### High Incident Alert
```yaml
automation:
  - alias: "High Incident Count Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.houston_active_incidents
        above: 50
    action:
      - service: notify.security_team
        data:
          message: "High incident count: {{ states('sensor.houston_active_incidents') }} active incidents"
```

## Dashboard Cards

### Trash Collection Card
```yaml
type: entities
title: Houston Trash Collection
entities:
  - entity: sensor.houston_trash_next_pickup
    name: Next Trash Pickup
  - entity: sensor.houston_recycling_next_pickup
    name: Next Recycling
  - entity: calendar.houston_trash_pickup_calendar
    name: Trash Calendar
```

### Heavy Trash Card
```yaml
type: entities
title: Heavy Trash Collection
entities:
  - entity: sensor.my_heavy_trash_route_status
    name: Collection Status
  - entity: sensor.my_heavy_trash_route_next_pickup
    name: Next Pickup
  - entity: sensor.my_heavy_trash_route_service_week
    name: Service Week
```

## Troubleshooting

### No Data Showing
- Verify your route ID is correct for heavy trash
- Check the API URL for trash collection
- Ensure you have internet connectivity
- Check Home Assistant logs for error messages

### Calendar Not Working
- Restart Home Assistant after installation
- Verify the calendar integration is enabled
- Check entity states in Developer Tools

### Heavy Trash Route Not Found
- Double-check your route ID format
- Verify the route exists in the [Houston Heavy Trash Dashboard](https://mycity.maps.arcgis.com/apps/dashboards/cb0ac86b3b434513b5f22428385820f3)
- Route IDs are case-sensitive

## Data Sources

- **Trash/Recycling**: City of Houston via Recollect API
- **Heavy Trash**: City of Houston ArcGIS Services
- **Incidents**: City of Houston Active Incidents API

## Contributing

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

- [Report Issues](https://gitea.shatto.cloud/Shatti/ha-custom-components/issues)
- [Feature Requests](https://gitea.shatto.cloud/Shatti/ha-custom-components/issues)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This integration is not officially affiliated with the City of Houston. Use of city data is subject to their terms of service and availability. 