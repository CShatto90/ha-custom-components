# Home Assistant Custom Components Collection

A collection of custom components for Home Assistant, created by Shatti.

## Installation

### HACS Installation (Recommended)
1. Open HACS in your Home Assistant instance
2. Click on the three dots in the top right corner
3. Select "Custom repositories"
4. Add this repository URL: `https://gitea.shatto.cloud/Shatti/ha-custom-components`
5. Select "Integration" as the category
6. Click "Add"
7. Find the component you want to install in HACS and click "Download"

### Manual Installation
1. Download this repository
2. Copy the contents of the `custom_components` folder to your Home Assistant's `custom_components` directory
3. Restart Home Assistant
4. Configure the components through the Home Assistant UI (Configuration -> Integrations)

## Available Components

### Houston Heavy Trash
Track Houston Heavy Trash pickup schedules and status. Provides sensors and calendar entries for your heavy trash pickup schedule.

[Documentation](#houston-heavy-trash-integration)

### Houston Trash
Track regular Houston trash pickup schedules. Provides sensors for your regular trash pickup schedule.

[Documentation](#houston-trash-integration)

### Houston Active Incidents
Monitor active incidents in Houston, including fire department and police department responses.

[Documentation](#houston-active-incidents-integration)

## Configuration

Each component has its own configuration instructions. Please refer to the individual component's documentation in its directory.

## Support

If you encounter any issues or have questions, please open an issue in this repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Houston Heavy Trash Integration

A Home Assistant integration for tracking Houston Heavy Trash pickup schedules and status.

## Installation

1. Download this repository
2. Copy the `houston_heavy_trash` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Finding Your Route ID

You can find your route ID using the City of Houston's [Heavy Trash Progress Dashboard](https://mycity.maps.arcgis.com/apps/dashboards/cb0ac86b3b434513b5f22428385820f3):

1. Open the dashboard in your web browser
2. Use the search function or zoom to your location
3. Click on your area to see the route information
4. The route ID will be in the format `SW4TH_08` where:
   - First two letters indicate the quadrant (NE, NW, SE, SW)
   - Next part indicates the week (1st, 2nd, 3rd, 4th)
   - Last part indicates the day (TH for Thursday, etc.)
   - Final number is the route number

## Configuration

Add the following to your `configuration.yaml`:

```yaml
houston_heavy_trash:
  routes:
    - name: "My Heavy Trash"  # Friendly name for the route
      route_id: "NE4TH_08"    # Route ID from the city's system
```

### Configuration Variables

| Variable | Required | Description |
|----------|----------|-------------|
| name | Yes | Friendly name for the route |
| route_id | Yes | Route ID from the city's system (e.g., NE4TH_08) |

## Available Components

### Sensors

For each configured route, the following sensors will be created:

- `sensor.{route_name}_status`: Current status of the heavy trash service
- `sensor.{route_name}_next_pickup`: Next scheduled pickup date
- `sensor.{route_name}_service_type`: Type of service (e.g., HT for Heavy Trash)
- `sensor.{route_name}_service_week`: Week of the month for service
- `sensor.{route_name}_service_day`: Day of the week for service
- `sensor.{route_name}_quadrant`: City quadrant (NE, NW, SE, SW)

### Calendar

A calendar entity is created for each route showing:
- Next scheduled pickup date
- Service completion status
- Service type and schedule information

# Houston Trash Integration

A Home Assistant integration for tracking regular Houston trash pickup schedules.

## Installation

1. Download this repository
2. Copy the `houston_trash` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Configuration

Add the following to your `configuration.yaml`:

```yaml
houston_trash:
  url: "https://api.recollect.net/api/areas/HoustonTX/services/1231/pages/en-US/place_calendar.json"
```

### Configuration Variables

| Variable | Required | Description |
|----------|----------|-------------|
| url | Yes | URL to the Recollect API |

## Available Components

### Sensors

For each configured route, the following sensors will be created:

- `sensor.{route_name}_status`: Current status of the trash service
- `sensor.{route_name}_next_pickup`: Next scheduled pickup date
- `sensor.{route_name}_service_type`: Type of service
- `sensor.{route_name}_service_week`: Week of the month for service
- `sensor.{route_name}_service_day`: Day of the week for service
- `sensor.{route_name}_quadrant`: City quadrant (NE, NW, SE, SW)

# Houston Active Incidents Integration

A Home Assistant integration for monitoring active incidents in Houston, including fire department and police department responses.

## Installation

1. Download this repository
2. Copy the `houston_incidents` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Configuration

Add the following to your `configuration.yaml`:

```yaml
sensor:
  - platform: houston_incidents
    name: "Houston Active Incidents"  # Optional, defaults to "Houston Active Incidents"
```

### Configuration Variables

| Variable | Required | Description |
|----------|----------|-------------|
| name | No | Friendly name for the sensor (defaults to "Houston Active Incidents") |

## Available Components

### Sensors

The following sensor will be created:

- `sensor.houston_active_incidents`: Shows total number of active incidents

### Attributes

The sensor includes the following attributes:

- `fd_incidents`: Number of active Fire Department incidents
- `pd_incidents`: Number of active Police Department incidents
- `incidents`: List of all active incidents with details including:
  - Agency (FD/PD)
  - Address
  - Cross Street
  - Key Map
  - Call Time (Opened)
  - Incident Type
  - Combined Response (Y/N) 