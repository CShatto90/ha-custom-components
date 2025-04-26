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

Components will be listed here as they are created.

## Configuration

Each component has its own configuration instructions. Please refer to the individual component's documentation in its directory.

## Support

If you encounter any issues or have questions, please open an issue in this repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Houston Heavy Trash

A Home Assistant integration for tracking Houston's Heavy Trash pickup schedules.

## Features

- Real-time status of heavy trash pickup for your route
- Multiple sensors providing detailed information:
  - Current pickup status
  - Service type
  - Today's service status
  - Tomorrow's service status
  - Service dates
  - Completion status
- Calendar integration showing upcoming pickup dates
- Automatic updates every 30 minutes

## Installation

### HACS (Recommended)
1. Open HACS in Home Assistant
2. Go to the Integrations tab
3. Click the three dots in the top right and select "Custom repositories"
4. Add this repository URL
5. Search for "Houston Heavy Trash" and install it
6. Restart Home Assistant

### Manual Installation
1. Download the `houston_heavy_trash` directory
2. Copy it to your `custom_components` directory in Home Assistant
3. Restart Home Assistant

## Configuration

1. Go to Home Assistant Settings > Devices & Services
2. Click "Add Integration"
3. Search for "Houston Heavy Trash"
4. Enter your route number (e.g., "NE4TH_08")
5. Click "Submit"

## Available Sensors

Each route will create the following sensors:

- **Heavy Trash Status**: Current status of pickup (e.g., "1-3 Days", "In Progress", "Completed")
- **Heavy Trash Service Type**: Type of service (e.g., "HT" for Heavy Trash)
- **Heavy Trash Serviced Today**: Whether service is happening today ("Yes"/"No")
- **Heavy Trash Serviced Tomorrow**: Whether service is scheduled for tomorrow ("Yes"/"No")
- **Heavy Trash Service Date**: The scheduled service date
- **Heavy Trash Tomorrow Service Date**: The next scheduled service date
- **Heavy Trash Service Completed**: Whether service has been completed ("Yes"/"No")
- **Heavy Trash Completed Date**: The date when service was completed

## Calendar Integration

The integration creates a calendar entity for each route that shows upcoming pickup dates:

- **In Progress**: Shows an event for today
- **Scheduled for Tomorrow**: Shows an event for tomorrow
- **1-3 Days**: Shows an event for 3 days from now
- **4-7 Days**: Shows an event spanning 4-7 days from now
- **Completed** or **8+ Days**: No calendar event is shown

The calendar events include:
- Route name in the event title
- Status description
- All-day events for easy visibility
- Automatic updates as the status changes

## Status Meanings

- **In Progress**: Pickup is happening today
- **Scheduled in X days**: Pickup is scheduled for tomorrow
- **1-3 Days**: Pickup is expected in 1-3 days
- **4-7 Days**: Pickup is expected in 4-7 days
- **8+ Days**: Pickup is more than a week away
- **Completed**: Pickup has been completed

## Support

If you encounter any issues or have questions:
1. Check the [Home Assistant forums](https://community.home-assistant.io/)
2. Open an issue in this repository

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 