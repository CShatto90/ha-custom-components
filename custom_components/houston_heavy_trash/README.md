# Houston Heavy Trash Collection

This component integrates Houston heavy trash collection schedule data into Home Assistant. It provides sensors and calendar entities for tracking heavy trash and tree waste collection schedules.

## Features
- Heavy trash collection schedule tracking
- Calendar integration
- Next pickup date sensors
- Differentiation between tree waste and junk waste months

## Installation
1. Add this repository to HACS
2. Install the "Houston Heavy Trash" integration
3. Add configuration to your `configuration.yaml`

## Configuration
```yaml
houston_heavy_trash:
  scan_interval: 3600  # Optional, defaults to 1 hour
```

## Available Entities
- Calendar showing heavy trash collection schedule
- Sensors for next pickup dates
- Binary sensors for collection day status
- Sensors for waste type (tree waste/junk waste) 