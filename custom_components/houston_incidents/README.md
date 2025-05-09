# Houston Incidents

This component integrates Houston incident data into Home Assistant. It provides sensors for tracking active incidents in the Houston area.

## Features
- Real-time incident tracking
- Configurable update intervals
- Detailed incident information

## Installation
1. Add this repository to HACS
2. Install the "Houston Incidents" integration
3. Add configuration to your `configuration.yaml`

## Configuration
```yaml
houston_incidents:
  scan_interval: 300  # Optional, defaults to 5 minutes
```

## Available Entities
- Sensor showing current active incidents
- Binary sensors for specific incident types 