# Houston Services for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant integration that provides Houston city services monitoring through a unified interface. Monitor trash collection, heavy trash schedules, active incidents, and flood warning gauges all from one integration.

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

### 🌊 Flood Warning System (FWS)
- Monitor Harris County flood gauge sensors in real-time
- Stream elevation readings with flood status alerts
- Multiple sensor support with customizable selections
- Flood level thresholds (Normal, Flooding Possible, Flooding Likely)

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
   - **Flood Warning System**: Monitor flood gauge sensors

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

#### Flood Warning System (FWS)
- **Select Sensors to Monitor**: Choose from popular flood gauge sensors
- **Custom Sensor**: Add additional sensors by ID and name

To find sensor IDs:
1. Visit the [Harris County FWS website](https://www.harriscountyfws.org)
2. Use the location dropdown to find sensors in your area
3. The sensor ID is the number in the URL (e.g., 582 for "582 Brickhouse Gully @ Hollister")

Popular sensors include:
- **582**: Brickhouse Gully @ Hollister
- **520**: White Oak Bayou @ Heights Boulevard  
- **430**: Brays Bayou @ Stella Link Road
- **740**: Lake Houston @ FM 1960
- **1050**: Spring Creek @ I-45

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

### Flood Warning System (FWS)
For each configured sensor:
- `sensor.[sensor_name]_stream_elevation` - Current stream elevation (feet)
- `sensor.[sensor_name]_flood_status` - Flood warning status
- `sensor.[sensor_name]_last_reading_time` - Timestamp of last sensor reading

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

### Flood Warning Alert
```yaml
automation:
  - alias: "Flood Warning Alert"
    trigger:
      - platform: state
        entity_id: sensor.brickhouse_gully_hollister_flood_status
        to: "Flooding Possible"
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "Flood warning: {{ trigger.to_state.attributes.location }} - {{ trigger.to_state.state }}"
          title: "⚠️ Flood Alert"

  - alias: "High Water Level Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.brickhouse_gully_hollister_stream_elevation
        above: 70.0
    action:
      - service: notify.family
        data:
          message: "High water level detected: {{ states('sensor.brickhouse_gully_hollister_stream_elevation') }} feet"
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

### Flood Warning Card
```yaml
type: entities
title: Houston Flood Monitoring
entities:
  - entity: sensor.brickhouse_gully_hollister_stream_elevation
    name: Stream Elevation
  - entity: sensor.brickhouse_gully_hollister_flood_status
    name: Flood Status
  - entity: sensor.white_oak_bayou_heights_boulevard_stream_elevation
    name: White Oak Elevation
  - entity: sensor.white_oak_bayou_heights_boulevard_flood_status
    name: White Oak Status
```

### Advanced Flood Gauge Card
```yaml
type: gauge
entity: sensor.brickhouse_gully_hollister_stream_elevation
name: Brickhouse Gully Water Level
unit: ft
min: 60
max: 80
severity:
  green: 0
  yellow: 70
  red: 76
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

### FWS Sensors Not Updating
- Verify sensor IDs are correct (numeric values like 582)
- Check that the sensor exists on the [Harris County FWS website](https://www.harriscountyfws.org)
- Some sensors may be temporarily offline for maintenance
- Check Home Assistant logs for HTTP errors

### FWS Data Parsing Issues
- The FWS website may have changed its format
- Check the integration logs for JSON parsing errors
- Try removing and re-adding problematic sensors

## Data Sources

- **Trash/Recycling**: City of Houston via Recollect API
- **Heavy Trash**: City of Houston ArcGIS Services
- **Incidents**: City of Houston Active Incidents API
- **Flood Warning System**: Harris County Flood Control District FWS

## Repository Information

**Developer**: Shatti (gitea.shatto.cloud) / Cshatto90 (GitHub)

This integration is primarily developed and maintained on a self-hosted Gitea instance at [gitea.shatto.cloud](https://gitea.shatto.cloud/Shatti/ha-custom-components). The code remains hosted on the developer's infrastructure for primary development and issue tracking.

**GitHub Mirror**: This repository is mirrored to GitHub specifically for HACS (Home Assistant Community Store) compatibility and distribution. The GitHub repository at [Cshatto90/ha-custom-components](https://github.com/Cshatto90/ha-custom-components) serves as the HACS installation source only.

**Note on GitHub Usage**: I apologize for any inconvenience, but I do not endorse GitHub's current use policies, particularly regarding AI training and business practices. This mirror exists solely for HACS compatibility. For detailed reasoning behind this position, please research GitHub's current policies regarding AI training on user repositories and related business practices.

### For Users:
- **Installation**: Use HACS with the GitHub repository (automatic)
- **Issues & Support**: Report to the primary Gitea repository (see Support section below)
- **Important**: GitHub issues may or may not be monitored - always use Gitea for reliable support

### For Developers:
- **Primary Repository**: [gitea.shatto.cloud/Shatti/ha-custom-components](https://gitea.shatto.cloud/Shatti/ha-custom-components)
- **Development**: All development, issues, and pull requests should target the Gitea repository
- **GitHub**: Read-only mirror for HACS distribution

## Contributing

**Primary Development Repository**: [gitea.shatto.cloud/Shatti/ha-custom-components](https://gitea.shatto.cloud/Shatti/ha-custom-components)

1. Fork the primary Gitea repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request to the Gitea repository

**Note**: Contributions should be made to the Gitea repository, not the GitHub mirror.

## Support

**Primary Support & Issues**: [gitea.shatto.cloud/Shatti/ha-custom-components](https://gitea.shatto.cloud/Shatti/ha-custom-components)

- [Report Issues](https://gitea.shatto.cloud/Shatti/ha-custom-components/issues)
- [Feature Requests](https://gitea.shatto.cloud/Shatti/ha-custom-components/issues)

**Developer Contact**: Shatti @ gitea.shatto.cloud

**Note**: While this integration is available through GitHub for HACS compatibility, all support, issues, and development discussions should be directed to the primary Gitea repository. **GitHub issues may or may not be monitored** - please use the Gitea repository for reliable support and issue tracking.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This integration is not officially affiliated with the City of Houston. Use of city data is subject to their terms of service and availability. 