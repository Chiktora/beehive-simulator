import requests
import time
import random
from datetime import datetime, timedelta
import math

# ThingSpeak settings
API_KEY = '2XT7DIZ2NLXKWZ6F'
BASE_URL = 'https://api.thingspeak.com/update'

class WeatherPattern:
    CLEAR = 'clear'
    CLOUDY = 'cloudy'
    RAINY = 'rainy'
    STORMY = 'stormy'

    def __init__(self):
        self.current_pattern = WeatherPattern.CLEAR
        self.pattern_duration = random.randint(360, 720)  # 6-12 hours
        self.pattern_time = 0
        self.next_patterns = {
            WeatherPattern.CLEAR: [WeatherPattern.CLEAR, WeatherPattern.CLOUDY],
            WeatherPattern.CLOUDY: [WeatherPattern.CLEAR, WeatherPattern.CLOUDY, WeatherPattern.RAINY],
            WeatherPattern.RAINY: [WeatherPattern.CLOUDY, WeatherPattern.RAINY, WeatherPattern.STORMY],
            WeatherPattern.STORMY: [WeatherPattern.RAINY, WeatherPattern.CLOUDY]
        }
        
    def update(self):
        """Update weather pattern"""
        self.pattern_time += 1
        if self.pattern_time >= self.pattern_duration:
            self.pattern_time = 0
            self.pattern_duration = random.randint(360, 720)
            self.current_pattern = random.choice(self.next_patterns[self.current_pattern])
            
    def get_pattern_effects(self):
        """Get current weather pattern effects"""
        effects = {
            WeatherPattern.CLEAR: {'temp_mod': 1, 'humidity_mod': -5},
            WeatherPattern.CLOUDY: {'temp_mod': 0, 'humidity_mod': 0},
            WeatherPattern.RAINY: {'temp_mod': -2, 'humidity_mod': 15},
            WeatherPattern.STORMY: {'temp_mod': -4, 'humidity_mod': 25}
        }
        return effects[self.current_pattern]

class WeatherTrend:
    def __init__(self):
        self.trend_duration = random.randint(180, 360)  # 3-6 hours
        self.trend_time = 0
        self.temp_trend = random.uniform(-3, 3)
        self.humidity_trend = random.uniform(-10, 10)
        self.wind_speed = random.uniform(0, 15)  # km/h
        self.wind_direction = random.uniform(0, 360)  # degrees
        self.pressure = random.uniform(995, 1025)  # hPa
        self.pressure_trend = random.uniform(-1, 1)
        
    def update(self):
        """Update trend progress and create new trend if needed"""
        self.trend_time += 1
        if self.trend_time >= self.trend_duration:
            self.trend_duration = random.randint(180, 360)
            self.trend_time = 0
            
            # Smooth transitions for new trends
            self.temp_trend = random.uniform(-3, 3)
            self.humidity_trend = random.uniform(-10, 10)
            
            # Update wind conditions
            self.wind_speed = max(0, min(30, self.wind_speed + random.uniform(-5, 5)))
            self.wind_direction = (self.wind_direction + random.uniform(-45, 45)) % 360
            
            # Update pressure trends
            self.pressure += self.pressure_trend
            self.pressure = max(985, min(1035, self.pressure))
            self.pressure_trend = random.uniform(-1, 1)
            
    def get_trend_factor(self):
        """Get current trend influence (0-1)"""
        return math.sin(math.pi * self.trend_time / self.trend_duration)
        
    def get_trends(self):
        """Get current weather trends"""
        factor = self.get_trend_factor()
        return {
            'temperature': self.temp_trend * factor,
            'humidity': self.humidity_trend * factor,
            'wind_speed': self.wind_speed,
            'wind_direction': self.wind_direction,
            'pressure': self.pressure,
            'pressure_trend': self.pressure_trend
        }

class WeatherConditions:
    def __init__(self):
        self.current_temp = 20
        self.current_humidity = 65
        self.target_temp = 20
        self.target_humidity = 65
        self.last_target_update = datetime.now()
        self.update_interval = 30
        self.weather_trend = WeatherTrend()
        self.weather_pattern = WeatherPattern()
        self.last_rain = datetime.now() - timedelta(days=1)
        
    def update_targets(self, base_temp, base_humidity, time_factor):
        """Update target values periodically"""
        now = datetime.now()
        minutes_passed = (now - self.last_target_update).total_seconds() / 60
        
        if minutes_passed >= self.update_interval:
            # Update weather patterns and trends
            self.weather_pattern.update()
            self.weather_trend.update()
            
            pattern_effects = self.weather_pattern.get_pattern_effects()
            trends = self.weather_trend.get_trends()
            
            # Calculate temperature variations
            daily_temp_variation = 6 if Season.get_current_season() == Season.WINTER else 10
            wind_chill = 0.5 * trends['wind_speed'] if trends['wind_speed'] > 10 else 0
            pressure_effect = (trends['pressure'] - 1013) / 100  # Slight effect from pressure
            
            # Set new temperature target
            self.target_temp = (
                base_temp +
                (daily_temp_variation * time_factor) +
                pattern_effects['temp_mod'] +
                trends['temperature'] -
                wind_chill +
                pressure_effect +
                random.uniform(-0.5, 0.5)
            )
            
            # Calculate humidity variations
            rain_effect = 0
            if self.weather_pattern.current_pattern in [WeatherPattern.RAINY, WeatherPattern.STORMY]:
                rain_effect = 20
                self.last_rain = now
            elif (now - self.last_rain).total_seconds() < 7200:  # 2 hours after rain
                rain_effect = 10 * math.exp(-(now - self.last_rain).total_seconds() / 3600)
            
            # Set new humidity target
            self.target_humidity = (
                base_humidity +
                (10 * (1 - time_factor)) +
                pattern_effects['humidity_mod'] +
                trends['humidity'] +
                rain_effect +
                random.uniform(-1, 1)
            )
            
            # Ensure values stay within realistic bounds
            self.target_humidity = max(30, min(95, self.target_humidity))
            self.last_target_update = now
    
    def get_current_conditions(self):
        """Get current conditions with smooth transitions"""
        # Calculate transition speed based on weather pattern
        if self.weather_pattern.current_pattern == WeatherPattern.STORMY:
            transition_speed = 0.05  # Faster changes during storms
        else:
            transition_speed = 0.02  # Normal smooth transitions
            
        # Gradually move current values towards targets
        self.current_temp += (self.target_temp - self.current_temp) * transition_speed
        self.current_humidity += (self.target_humidity - self.current_humidity) * transition_speed
        
        return {
            'temperature': self.current_temp,
            'humidity': self.current_humidity,
            'pattern': self.weather_pattern.current_pattern,
            'trends': self.weather_trend.get_trends()
        }

class Season:
    WINTER = 'winter'
    SPRING = 'spring'
    SUMMER = 'summer'
    FALL = 'fall'

    @staticmethod
    def get_current_season():
        month = datetime.now().month
        if month in [12, 1, 2]:
            return Season.WINTER
        elif month in [3, 4, 5]:
            return Season.SPRING
        elif month in [6, 7, 8]:
            return Season.SUMMER
        else:
            return Season.FALL

    @staticmethod
    def get_season_progress():
        """Calculate progress through current season (0-1)"""
        month = datetime.now().month
        day = datetime.now().day
        
        # Calculate days into current season
        if month in [12, 1, 2]:  # Winter
            if month == 12:
                days = day
            else:
                days = day + (month * 31)
        else:
            days = day + ((month % 3) * 31)
            
        return days / 90  # Approximate season length

class HiveEvent:
    def __init__(self):
        self.current_events = []  # Allow multiple concurrent events
        self.event_durations = {}
        self.event_times = {}
        self.last_season = None
        self.season_started = datetime.now()
        self.daily_event_checks = {
            'nectar_flow': False,
            'pollen_collection': False,
            'propolis_collection': False
        }
        
        # Define incompatible event combinations
        self.incompatible_events = {
            'swarming': ['winter_cluster', 'honey_harvesting', 'robbing', 'queen_mating'],
            'winter_cluster': ['swarming', 'nectar_flow', 'queen_mating', 'pollen_collection', 'propolis_collection'],
            'queen_mating': ['winter_cluster', 'swarming', 'honey_harvesting'],
            'honey_harvesting': ['swarming', 'queen_mating', 'nectar_flow'],
            'robbing': ['swarming', 'nectar_flow'],
            'ventilation': []  # Compatible with all
        }
        
        # Define event synergies (events that enhance each other's effects)
        self.event_synergies = {
            'nectar_flow': {
                'pollen_collection': {'weight_mod': 1.2},  # 20% bonus to weight gain
                'ventilation': {'humidity_mod': 1.5}  # 50% more effective humidity reduction
            },
            'brood_rearing': {
                'pollen_collection': {'inside_temp_mod': 1.3},  # 30% more heat generation
                'nectar_flow': {'weight_mod': 1.2}  # 20% more weight gain
            },
            'ventilation': {
                'propolis_collection': {'inside_humidity_mod': 1.2}  # 20% more effective humidity control
            }
        }

    def reset_daily_checks(self):
        """Reset daily event checks at midnight"""
        current_hour = datetime.now().hour
        if current_hour == 0:
            self.daily_event_checks = {k: False for k in self.daily_event_checks}

    def check_seasonal_transition(self):
        """Check if season has changed and trigger relevant events"""
        current_season = Season.get_current_season()
        if current_season != self.last_season:
            self.last_season = current_season
            self.season_started = datetime.now()
            
            # Trigger seasonal events
            if current_season == Season.SPRING:
                if random.random() < 0.3:  # 30% chance of swarming in spring
                    self.add_event('swarming')
                self.add_event('spring_buildup')
            elif current_season == Season.WINTER:
                self.add_event('winter_cluster')

    def is_event_compatible(self, new_event):
        """Check if a new event is compatible with current events"""
        if new_event not in self.incompatible_events:
            return True
            
        for current_event in self.current_events:
            if current_event in self.incompatible_events[new_event]:
                return False
        return True

    def check_for_new_event(self):
        """Check for new events based on season and conditions"""
        self.reset_daily_checks()
        self.check_seasonal_transition()
        current_season = Season.get_current_season()
        
        # Define event probabilities based on season (chance per minute)
        base_probabilities = {
            'swarming': 0.000001 if current_season == Season.SPRING else 0,
            'nectar_flow': 0.001 if current_season in [Season.SPRING, Season.SUMMER] else 0,
            'queen_mating': 0.000001 if current_season == Season.SPRING else 0,
            'brood_rearing': 0.001 if current_season != Season.WINTER else 0,
            'honey_harvesting': 0.0001 if current_season in [Season.SUMMER, Season.FALL] else 0,
            'pollen_collection': 0.002 if current_season != Season.WINTER else 0,
            'propolis_collection': 0.001 if current_season != Season.WINTER else 0,
            'ventilation': 0.002 if current_season != Season.WINTER else 0.0005,
            'robbing': 0.0001 if current_season in [Season.SUMMER, Season.FALL] else 0,
            'varroa_infestation': 0.00001,  # Year-round but rare
            'nosema': 0.000005 if current_season in [Season.WINTER, Season.SPRING] else 0
        }

        # Adjust probabilities based on current events
        if 'nectar_flow' in self.current_events:
            base_probabilities['pollen_collection'] *= 1.5  # More likely during nectar flow
            base_probabilities['ventilation'] *= 1.3  # More ventilation needed
        
        if 'brood_rearing' in self.current_events:
            base_probabilities['pollen_collection'] *= 1.4  # More pollen needed for brood
            base_probabilities['nectar_flow'] *= 1.2  # More nectar needed

        # Check for new events
        for event, probability in base_probabilities.items():
            # Skip if event check already done today or event is already active
            if (event in self.daily_event_checks and self.daily_event_checks[event]) or event in self.current_events:
                continue
                
            if random.random() < probability and self.is_event_compatible(event):
                self.add_event(event)
                if event in self.daily_event_checks:
                    self.daily_event_checks[event] = True

    def add_event(self, event):
        """Add a new event with appropriate duration"""
        if event not in self.current_events:
            self.current_events.append(event)
            
            # Set event duration (in minutes)
            durations = {
                'swarming': random.randint(120, 240),          # 2-4 hours
                'nectar_flow': random.randint(720, 2880),      # 12-48 hours
                'queen_mating': random.randint(30, 60),        # 30-60 minutes
                'brood_rearing': random.randint(4320, 5760),   # 3-4 days
                'honey_harvesting': random.randint(180, 360),  # 3-6 hours
                'winter_cluster': random.randint(43200, 86400),# 30-60 days
                'spring_buildup': random.randint(20160, 40320),# 14-28 days
                'pollen_collection': random.randint(360, 720), # 6-12 hours
                'propolis_collection': random.randint(180, 360),# 3-6 hours
                'ventilation': random.randint(20, 40),         # 20-40 minutes
                'robbing': random.randint(120, 360),          # 2-6 hours
                'varroa_infestation': random.randint(10080, 20160), # 7-14 days
                'nosema': random.randint(4320, 8640)          # 3-6 days
            }
            
            self.event_durations[event] = durations.get(event, 60)
            self.event_times[event] = 0
            print(f"\nNew event started: {event} (Duration: {self.event_durations[event]} minutes)")

    def update(self):
        """Update all current events"""
        for event in list(self.current_events):  # Create a copy to allow modification during iteration
            self.event_times[event] += 1
            if self.event_times[event] >= self.event_durations[event]:
                print(f"\nEvent ended: {event}")
                self.current_events.remove(event)
                del self.event_durations[event]
                del self.event_times[event]

    def get_event_effects(self):
        """Return combined modifications to sensor values based on all current events"""
        effects = {
            'inside_temp_mod': 0,
            'inside_humidity_mod': 0,
            'weight_mod': 0
        }

        # Calculate base effects for each event
        for event in self.current_events:
            progress = self.event_times[event] / self.event_durations[event]
            
            # Store individual event effects for potential synergy calculations
            event_effects = {
                'inside_temp_mod': 0,
                'inside_humidity_mod': 0,
                'weight_mod': 0
            }

            if event == 'swarming':
                event_effects['inside_temp_mod'] = 4 * math.sin(progress * math.pi)
                event_effects['inside_humidity_mod'] = -5 * math.sin(progress * math.pi)
                event_effects['weight_mod'] = -3 * (progress if progress < 0.5 else 1)

            elif event == 'nectar_flow':
                event_effects['inside_temp_mod'] = 1
                event_effects['inside_humidity_mod'] = 3
                event_effects['weight_mod'] = 0.05 * progress

            elif event == 'queen_mating':
                event_effects['inside_temp_mod'] = 2 * math.sin(progress * math.pi)

            elif event == 'brood_rearing':
                event_effects['inside_temp_mod'] = 2
                event_effects['inside_humidity_mod'] = 5
                event_effects['weight_mod'] = -0.01

            elif event == 'honey_harvesting':
                event_effects['inside_temp_mod'] = 1
                event_effects['inside_humidity_mod'] = -3
                event_effects['weight_mod'] = -0.1 * progress

            elif event == 'winter_cluster':
                event_effects['inside_temp_mod'] = -5
                event_effects['inside_humidity_mod'] = 8
                event_effects['weight_mod'] = -0.02 * progress

            elif event == 'spring_buildup':
                event_effects['inside_temp_mod'] = progress * 3
                event_effects['inside_humidity_mod'] = 2
                event_effects['weight_mod'] = 0.03 * progress

            elif event in ['pollen_collection', 'propolis_collection']:
                event_effects['inside_temp_mod'] = 0.5
                event_effects['weight_mod'] = 0.01

            elif event == 'ventilation':
                event_effects['inside_temp_mod'] = -2 * math.sin(progress * math.pi)
                event_effects['inside_humidity_mod'] = -8 * math.sin(progress * math.pi)

            elif event == 'robbing':
                event_effects['inside_temp_mod'] = 2
                event_effects['weight_mod'] = -0.05 * progress

            elif event == 'varroa_infestation':
                event_effects['inside_humidity_mod'] = 5
                event_effects['weight_mod'] = -0.02 * progress

            elif event == 'nosema':
                event_effects['inside_humidity_mod'] = 8
                event_effects['weight_mod'] = -0.03 * progress

            # Apply synergy effects if applicable
            if event in self.event_synergies:
                for other_event in self.current_events:
                    if other_event in self.event_synergies[event]:
                        synergy = self.event_synergies[event][other_event]
                        for mod_type, multiplier in synergy.items():
                            event_effects[mod_type] *= multiplier

            # Add event effects to total effects
            for key in effects:
                effects[key] += event_effects[key]

        return effects

class HiveWeight:
    def __init__(self):
        self.base_weight = 30  # Base hive weight in kg
        self.honey_stores = 15  # Initial honey stores in kg
        self.pollen_stores = 2  # Initial pollen stores in kg
        self.bee_population = 1  # Initial bee mass in kg (approximately 10,000 bees)
        self.brood_mass = 0.5   # Initial brood mass in kg
        self.moisture_content = 0  # Additional weight from moisture
        
    def calculate_daily_consumption(self, season, is_winter_cluster):
        """Calculate daily food consumption"""
        if is_winter_cluster:
            return 0.05  # 50g per day in winter cluster
        
        consumption_rates = {
            Season.WINTER: 0.03,  # 30g per day
            Season.SPRING: 0.1,   # 100g per day (high due to brood rearing)
            Season.SUMMER: 0.08,  # 80g per day
            Season.FALL: 0.05     # 50g per day
        }
        return consumption_rates[season]
    
    def update_weight(self, events, weather_pattern, time_factor, season):
        """Update hive weight based on various factors"""
        # Calculate base daily changes
        daily_consumption = self.calculate_daily_consumption(
            season, 'winter_cluster' in events
        ) / 1440  # Convert daily rate to per-minute rate
        
        # Consume stores
        self.honey_stores = max(0, self.honey_stores - daily_consumption)
        
        # Process each event's effect on weight
        for event in events:
            if event == 'nectar_flow':
                # Gain honey stores during nectar flow
                if time_factor > 0:  # Only during daylight
                    nectar_collection = 0.002 * time_factor  # Up to 2g per minute at peak
                    self.honey_stores += nectar_collection
            
            elif event == 'pollen_collection':
                # Gain pollen stores during collection
                if time_factor > 0:  # Only during daylight
                    pollen_collection = 0.001 * time_factor  # Up to 1g per minute at peak
                    self.pollen_stores += pollen_collection
            
            elif event == 'brood_rearing':
                # Convert food stores to brood mass
                food_to_brood = 0.0003  # 0.3g per minute
                if self.honey_stores > food_to_brood and self.pollen_stores > food_to_brood * 0.5:
                    self.honey_stores -= food_to_brood
                    self.pollen_stores -= food_to_brood * 0.5
                    self.brood_mass += food_to_brood * 0.3  # 30% efficiency
            
            elif event == 'honey_harvesting':
                # Rapid honey removal during harvest
                self.honey_stores = max(5, self.honey_stores - 0.05)  # Leave 5kg minimum
            
            elif event == 'swarming':
                # Lose approximately half of bee population
                if self.bee_population > 0.5:  # Only if enough bees
                    self.bee_population *= 0.5
            
            elif event == 'spring_buildup':
                # Gradual increase in bee population
                if self.honey_stores > 0.1 and self.pollen_stores > 0.05:
                    population_growth = 0.0001  # 0.1g per minute
                    self.bee_population += population_growth
                    self.honey_stores -= population_growth * 2
                    self.pollen_stores -= population_growth
        
        # Process weather effects
        if weather_pattern in [WeatherPattern.RAINY, WeatherPattern.STORMY]:
            self.moisture_content = min(0.5, self.moisture_content + 0.001)  # Up to 0.5kg of moisture
        else:
            self.moisture_content = max(0, self.moisture_content - 0.0005)  # Gradual drying
        
        # Natural losses
        self.bee_population = max(0.5, self.bee_population - 0.00002)  # Natural bee mortality
        self.pollen_stores = max(0, self.pollen_stores - 0.00001)  # Pollen degradation
        
        # Ensure realistic limits
        self.honey_stores = min(25, self.honey_stores)  # Max 25kg honey
        self.pollen_stores = min(5, self.pollen_stores)  # Max 5kg pollen
        self.bee_population = min(2, self.bee_population)  # Max 2kg bees
        self.brood_mass = min(1, self.brood_mass)  # Max 1kg brood
        
        # Calculate total weight
        total_weight = (self.base_weight + 
                       self.honey_stores + 
                       self.pollen_stores + 
                       self.bee_population + 
                       self.brood_mass + 
                       self.moisture_content)
        
        return total_weight

def get_time_factor():
    """Calculate time-based factors for daily cycles (0.0 to 1.0)"""
    current_time = datetime.now()
    hour = current_time.hour + current_time.minute / 60.0
    
    # Adjust peak time and daylight hours based on season
    season = Season.get_current_season()
    season_progress = Season.get_season_progress()
    
    if season == Season.SUMMER:
        peak_hour = 14
        day_length = 15  # Longer summer days
    elif season == Season.WINTER:
        peak_hour = 12
        day_length = 9   # Shorter winter days
    else:
        # Spring and Fall: interpolate between summer and winter
        if season == Season.SPRING:
            progress_factor = season_progress
        else:  # FALL
            progress_factor = 1 - season_progress
            
        peak_hour = 12 + (2 * progress_factor)
        day_length = 9 + (6 * progress_factor)
    
    # Calculate sunrise and sunset times
    sunrise = (24 - day_length) / 2
    sunset = sunrise + day_length
    
    # Calculate time factor
    if hour < sunrise or hour > sunset:
        return 0  # Night time
    else:
        # Adjust sine wave to fit between sunrise and sunset
        day_progress = (hour - sunrise) / day_length
        return math.sin(day_progress * math.pi) * 0.5 + 0.5

def get_seasonal_base_values():
    """Get base values adjusted for current season in Bulgaria"""
    season = Season.get_current_season()
    season_progress = Season.get_season_progress()
    
    if season == Season.WINTER:
        base_temp = 0 + (5 * season_progress)  # Gradually warming
        humidity = 80 - (10 * season_progress)
    elif season == Season.SPRING:
        base_temp = 5 + (20 * season_progress)  # Warming up
        humidity = 70 - (10 * season_progress)
    elif season == Season.SUMMER:
        base_temp = 25 + (8 * math.sin(season_progress * math.pi))  # Peak in mid-summer
        humidity = 60 + (5 * math.sin(season_progress * math.pi))
    else:  # FALL
        base_temp = 25 - (20 * season_progress)  # Cooling down
        humidity = 65 + (15 * season_progress)
    
    return {
        'temp': base_temp,
        'humidity': humidity
    }

def simulate_sensors(hive_event):
    """Simulate beehive sensor readings"""
    time_factor = get_time_factor()
    event_effects = hive_event.get_event_effects()
    seasonal_base = get_seasonal_base_values()
    
    # Update weather conditions
    weather.update_targets(seasonal_base['temp'], seasonal_base['humidity'], time_factor)
    current_weather = weather.get_current_conditions()
    
    # Get weather details
    outside_temp = current_weather['temperature']
    outside_humidity = current_weather['humidity']
    weather_pattern = current_weather['pattern']
    trends = current_weather['trends']
    
    # Calculate inside temperature with weather influences
    base_inside_temp = 35  # Base temperature bees try to maintain
    
    # Adjust inside temperature based on outside conditions
    temp_difference = base_inside_temp - outside_temp
    energy_factor = math.exp(-abs(temp_difference) / 10)  # How hard bees need to work
    
    # Calculate inside conditions
    inside_temp = (base_inside_temp + 
                  event_effects['inside_temp_mod'] + 
                  (0.1 * trends['wind_speed'] if weather_pattern in [WeatherPattern.STORMY, WeatherPattern.RAINY] else 0) +
                  random.uniform(-0.3, 0.3))
    
    inside_humidity = (60 + 
                      event_effects['inside_humidity_mod'] +
                      (5 if weather_pattern in [WeatherPattern.RAINY, WeatherPattern.STORMY] else 0) +
                      random.uniform(-0.5, 0.5))
    
    # Calculate weight using the new weight management system
    weight = hive_weight.update_weight(
        hive_event.current_events,
        weather_pattern,
        time_factor,
        Season.get_current_season()
    )
    
    # Ensure values stay within realistic bounds
    inside_humidity = max(40, min(90, inside_humidity))
    inside_temp = max(25, min(40, inside_temp))
    weight = max(20, min(50, weight))
    
    return {
        'field1': round(inside_temp, 2),
        'field2': round(inside_humidity, 2),
        'field3': round(outside_temp, 2),
        'field4': round(outside_humidity, 2),
        'field5': round(weight, 2)
    }

def send_to_thingspeak(data):
    """Send data to ThingSpeak"""
    params = {
        'api_key': API_KEY,
        **data
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            print(f"Data sent successfully: {data}")
        else:
            print(f"Failed to send data: {response.status_code}")
    except Exception as e:
        print(f"Error sending data: {e}")

def main():
    print("Starting BeeHive Simulator...")
    print("Press Ctrl+C to stop")
    
    global weather, hive_weight
    weather = WeatherConditions()
    hive_weight = HiveWeight()
    hive_event = HiveEvent()
    
    while True:
        hive_event.check_for_new_event()
        hive_event.update()
        data = simulate_sensors(hive_event)
        send_to_thingspeak(data)
        time.sleep(60)  # Wait for 1 minute

if __name__ == "__main__":
    main() 