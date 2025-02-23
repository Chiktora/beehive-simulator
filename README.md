# Beehive Data Simulator Documentation

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Key Features](#key-features)
4. [Detailed System Components](#detailed-system-components)
5. [Data Generation](#data-generation)
6. [Configuration](#configuration)
7. [Technical Details](#technical-details)

## Overview

The Beehive Data Simulator is a sophisticated tool designed to generate realistic sensor data for beehive monitoring systems. It simulates the complex interactions between environmental conditions, bee colony activities, and seasonal patterns specific to Bulgarian climate conditions. The simulator provides real-time data that mirrors actual beehive behavior, making it ideal for testing monitoring systems, research purposes, and educational applications.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Chiktora/beehive-simulator.git
cd beehive-simulator
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your ThingSpeak API key in `beehive_simulator.py`:
```python
API_KEY = 'YOUR_API_KEY'
```

4. Run the simulator:
```bash
python beehive_simulator.py
```

## Key Features

### 1. Environmental Simulation

#### Weather Patterns
- **Clear Weather**
  - Temperature modifier: +1°C
  - Humidity modifier: -5%
  - Optimal for foraging activities

- **Cloudy Conditions**
  - Neutral temperature effect
  - Neutral humidity effect
  - Reduced foraging efficiency

- **Rainy Weather**
  - Temperature modifier: -2°C
  - Humidity modifier: +15%
  - Increased moisture content

- **Stormy Conditions**
  - Temperature modifier: -4°C
  - Humidity modifier: +25%
  - Rapid weather transitions

#### Weather Trends
- Wind speed simulation (0-30 km/h)
- Wind direction (0-360 degrees)
- Atmospheric pressure (985-1035 hPa)
- Temperature variations (±3°C)
- Humidity fluctuations (±10%)

### 2. Seasonal Patterns

#### Winter (December-February)
- Temperature range: 0-5°C
- Humidity: 70-80%
- Daylight: 9 hours
- Solar peak: 12:00
- Primary activity: Winter clustering

#### Spring (March-May)
- Temperature: 5-25°C (progressive warming)
- Humidity: 60-70%
- Daylight: 9-15 hours (increasing)
- Solar peak: 12:00-14:00
- Key activities: Brood rearing, swarming

#### Summer (June-August)
- Temperature: 25-33°C
- Humidity: 60-65%
- Daylight: 15 hours
- Solar peak: 14:00
- Peak foraging and honey production

#### Fall (September-November)
- Temperature: 25-5°C (progressive cooling)
- Humidity: 65-80%
- Daylight: 15-9 hours (decreasing)
- Solar peak: 14:00-12:00
- Focus: Winter preparation

## Detailed System Components

### 1. Weight Management System

#### Base Components
| Component | Range (kg) | Description |
|-----------|------------|-------------|
| Base Weight | 30 | Fixed hive structure |
| Honey Stores | 0-25 | Variable honey reserves |
| Pollen Stores | 0-5 | Stored pollen |
| Bee Population | 0.5-2 | Live bee mass |
| Brood Mass | 0-1 | Developing bees |
| Moisture | 0-0.5 | Environmental moisture |

#### Daily Consumption Rates
| Season | Consumption (g/day) | Notes |
|--------|-------------------|-------|
| Winter Cluster | 50 | Minimal activity |
| Winter | 30 | Base survival |
| Spring | 100 | High brood rearing |
| Summer | 80 | Active foraging |
| Fall | 50 | Preparation phase |

### 2. Event System

#### Regular Events
- **Nectar Flow**
  - Occurrence: Spring/Summer
  - Weight gain: 2g/minute max
  - Daylight dependent
  - Affects: Honey stores

- **Pollen Collection**
  - Active season collection
  - Weight gain: 1g/minute max
  - Daylight dependent
  - Affects: Pollen stores

- **Brood Rearing**
  - Resource consumption: 0.3g/minute
  - Conversion efficiency: 30%
  - Affects: Population growth

#### Special Events
- **Swarming**
  - Spring occurrence
  - Population impact: -50%
  - Temperature increase: +4°C
  - Duration: 2-4 hours

- **Winter Cluster**
  - Duration: 30-60 days
  - Temperature maintenance
  - Reduced consumption
  - Limited activity

### 3. Event Synergies

#### Compatible Combinations
```
Nectar Flow + Pollen Collection:
- Weight gain bonus: 20%
- Increased ventilation needs

Brood Rearing + Pollen Collection:
- Temperature efficiency: +30%
- Resource consumption: +40%

Ventilation + Propolis Collection:
- Humidity control: +20%
- Temperature regulation bonus
```

## Data Generation

### 1. Sensor Data Output
```json
{
    "field1": "Inside Temperature (°C)",
    "field2": "Inside Humidity (%)",
    "field3": "Outside Temperature (°C)",
    "field4": "Outside Humidity (%)",
    "field5": "Total Weight (kg)"
}
```

### 2. Update Frequency
- Data generation: Every minute
- ThingSpeak upload: Real-time
- Weather updates: Every 30 minutes
- Event checks: Continuous

### 3. Value Ranges
| Parameter | Min | Max | Normal Range |
|-----------|-----|-----|--------------|
| Inside Temp | 25°C | 40°C | 34-36°C |
| Inside Humidity | 40% | 90% | 55-65% |
| Weight | 20kg | 50kg | 30-45kg |

## Configuration

### 1. ThingSpeak Settings
```python
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://api.thingspeak.com/update'
```

### 2. Simulation Parameters
```python
UPDATE_INTERVAL = 60  # seconds
WEATHER_UPDATE = 30   # minutes
MAX_HONEY = 25       # kg
MAX_POLLEN = 5       # kg
BASE_WEIGHT = 30     # kg
```

## Technical Details

### 1. Dependencies
- Python 3.6+
- Required packages:
  ```
  requests==2.31.0
  ```

### 2. Code Structure
```
beehive_simulator/
├── beehive_simulator.py
├── requirements.txt
└── README.md
```

### 3. Classes
- `WeatherPattern`: Weather condition management
- `WeatherTrend`: Long-term weather trends
- `Season`: Seasonal calculations
- `HiveWeight`: Weight component tracking
- `HiveEvent`: Event management and effects

### 4. Error Handling
- API communication retry logic
- Data validation
- Boundary checking
- Exception logging

### 5. Performance
- Memory usage: ~50MB
- CPU usage: Low
- Network: ~1KB per minute

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to our repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Beekeeping expertise provided by BUZZWatch
- Weather data patterns based on Bulgarian meteorological records
- Bee behavior models based on scientific research

---

*Last updated: 21.02.2025*
*Version: 1.0.0* 
