"""
Routing API Integration Module
Calculates optimal routes for emergency responders
Supports Google Maps API and OpenRouteService API
"""

import requests
import os
import math
from datetime import datetime

class RoutingAPI:
    """
    Routing API client for calculating optimal emergency response routes
    Supports multiple routing services
    """
    
    def __init__(self, service='google', api_key=None):
        """
        Initialize Routing API client
        
        Args:
            service: Routing service to use ('google' or 'openroute')
            api_key: API key for the selected service
        """
        self.service = service
        
        if service == 'google':
            self.api_key = api_key or os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_GOOGLE_MAPS_API_KEY_HERE')
            self.base_url = "https://maps.googleapis.com/maps/api"
        elif service == 'openroute':
            self.api_key = api_key or os.getenv('OPENROUTE_API_KEY', 'YOUR_OPENROUTE_API_KEY_HERE')
            self.base_url = "https://api.openrouteservice.org"
        else:
            print(f"Unknown routing service: {service}")
            self.api_key = None
        
        self.enabled = self.api_key not in ['YOUR_GOOGLE_MAPS_API_KEY_HERE', 'YOUR_OPENROUTE_API_KEY_HERE', None]
        
        if not self.enabled:
            print("Routing API not configured. Using simulated routes.")
            print(f"To enable: Set {service.upper()}_API_KEY environment variable")
    
    def get_optimal_route(self, start_coords, end_coords, mode='driving', optimize_for='time'):
        """
        Calculate the optimal route between two points
        
        Args:
            start_coords: Tuple of (latitude, longitude) for start point
            end_coords: Tuple of (latitude, longitude) for end point
            mode: Transportation mode ('driving', 'walking', 'bicycling')
            optimize_for: Optimization criteria ('time' or 'distance')
        
        Returns:
            dict: Route information including distance, duration, and coordinates
        """
        if not self.enabled:
            return self._get_simulated_route(start_coords, end_coords)
        
        if self.service == 'google':
            return self._get_google_route(start_coords, end_coords, mode, optimize_for)
        elif self.service == 'openroute':
            return self._get_openroute_route(start_coords, end_coords, mode)
        else:
            return self._get_simulated_route(start_coords, end_coords)
    
    def _get_google_route(self, start_coords, end_coords, mode, optimize_for):
        """Get route using Google Maps Directions API"""
        try:
            url = f"{self.base_url}/directions/json"
            
            params = {
                'origin': f"{start_coords[0]},{start_coords[1]}",
                'destination': f"{end_coords[0]},{end_coords[1]}",
                'mode': mode,
                'alternatives': True,
                'key': self.api_key
            }
            
            # Add traffic model for driving
            if mode == 'driving':
                params['departure_time'] = 'now'
                params['traffic_model'] = 'best_guess'
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'OK' and data['routes']:
                    # Select best route based on optimization criteria
                    route = data['routes'][0]
                    leg = route['legs'][0]
                    
                    # Extract route coordinates from polyline
                    polyline = route['overview_polyline']['points']
                    coordinates = self._decode_polyline(polyline)
                    
                    route_data = {
                        'distance': leg['distance']['value'] / 1000,  # Convert to km
                        'duration': leg['duration']['value'] / 60,  # Convert to minutes
                        'duration_in_traffic': leg.get('duration_in_traffic', {}).get('value', leg['duration']['value']) / 60,
                        'start_address': leg['start_address'],
                        'end_address': leg['end_address'],
                        'coordinates': coordinates,
                        'steps': self._extract_steps(leg['steps']),
                        'warnings': route.get('warnings', []),
                        'service': 'google'
                    }
                    
                    return route_data
                else:
                    print(f"Google API status: {data['status']}")
                    return self._get_simulated_route(start_coords, end_coords)
            else:
                print(f"Google API error: {response.status_code}")
                return self._get_simulated_route(start_coords, end_coords)
                
        except Exception as e:
            print(f"Error fetching Google route: {e}")
            return self._get_simulated_route(start_coords, end_coords)
    
    def _get_openroute_route(self, start_coords, end_coords, mode):
        """Get route using OpenRouteService API"""
        try:
            # Convert mode to OpenRouteService profile
            profile_map = {
                'driving': 'driving-car',
                'walking': 'foot-walking',
                'bicycling': 'cycling-regular'
            }
            profile = profile_map.get(mode, 'driving-car')
            
            url = f"{self.base_url}/v2/directions/{profile}"
            
            headers = {
                'Authorization': self.api_key,
                'Content-Type': 'application/json'
            }
            
            body = {
                'coordinates': [
                    [start_coords[1], start_coords[0]],  # ORS uses [lon, lat]
                    [end_coords[1], end_coords[0]]
                ],
                'instructions': True,
                'elevation': False
            }
            
            response = requests.post(url, json=body, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'routes' in data and data['routes']:
                    route = data['routes'][0]
                    
                    # Extract coordinates
                    coordinates = [
                        (coord[1], coord[0])  # Convert back to [lat, lon]
                        for coord in route['geometry']['coordinates']
                    ]
                    
                    route_data = {
                        'distance': route['summary']['distance'] / 1000,  # Convert to km
                        'duration': route['summary']['duration'] / 60,  # Convert to minutes
                        'coordinates': coordinates,
                        'steps': self._extract_openroute_steps(route.get('segments', [])),
                        'service': 'openroute'
                    }
                    
                    return route_data
                else:
                    return self._get_simulated_route(start_coords, end_coords)
            else:
                print(f"OpenRoute API error: {response.status_code}")
                return self._get_simulated_route(start_coords, end_coords)
                
        except Exception as e:
            print(f"Error fetching OpenRoute route: {e}")
            return self._get_simulated_route(start_coords, end_coords)
    
    def _get_simulated_route(self, start_coords, end_coords):
        """
        Generate simulated route when API is not available
        Uses Haversine formula for distance and simple path interpolation
        
        Args:
            start_coords: Tuple of (latitude, longitude)
            end_coords: Tuple of (latitude, longitude)
        
        Returns:
            dict: Simulated route data
        """
        # Calculate straight-line distance using Haversine formula
        distance_km = self._haversine_distance(start_coords, end_coords)
        
        # Estimate actual road distance (typically 1.3x straight line)
        road_distance = distance_km * 1.3
        
        # Estimate duration (assuming average speed of 40 km/h in city)
        duration_minutes = (road_distance / 40) * 60
        
        # Generate intermediate waypoints for visualization
        num_waypoints = max(5, int(distance_km * 2))
        coordinates = self._interpolate_path(start_coords, end_coords, num_waypoints)
        
        route_data = {
            'distance': round(road_distance, 2),
            'duration': round(duration_minutes, 1),
            'duration_in_traffic': round(duration_minutes * 1.2, 1),  # Add 20% for traffic
            'coordinates': coordinates,
            'steps': [
                {
                    'instruction': 'Head to emergency location',
                    'distance': road_distance,
                    'duration': duration_minutes
                }
            ],
            'service': 'simulated',
            'simulated': True
        }
        
        return route_data
    
    def _haversine_distance(self, coord1, coord2):
        """
        Calculate distance between two coordinates using Haversine formula
        
        Args:
            coord1: Tuple of (latitude, longitude)
            coord2: Tuple of (latitude, longitude)
        
        Returns:
            float: Distance in kilometers
        """
        # Earth radius in kilometers
        R = 6371.0
        
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        distance = R * c
        return distance
    
    def _interpolate_path(self, start_coords, end_coords, num_points):
        """
        Create interpolated path between two points
        
        Args:
            start_coords: Start coordinates
            end_coords: End coordinates
            num_points: Number of intermediate points
        
        Returns:
            list: List of (lat, lon) tuples
        """
        path = []
        
        for i in range(num_points + 1):
            t = i / num_points
            
            lat = start_coords[0] + t * (end_coords[0] - start_coords[0])
            lon = start_coords[1] + t * (end_coords[1] - start_coords[1])
            
            # Add slight randomness to simulate road curvature
            if 0 < i < num_points:
                import random
                lat += random.uniform(-0.001, 0.001)
                lon += random.uniform(-0.001, 0.001)
            
            path.append((lat, lon))
        
        return path
    
    def _decode_polyline(self, polyline_str):
        """
        Decode Google Maps polyline string to coordinates
        
        Args:
            polyline_str: Encoded polyline string
        
        Returns:
            list: List of (lat, lon) tuples
        """
        coordinates = []
        index = 0
        lat = 0
        lng = 0
        
        while index < len(polyline_str):
            b = 0
            shift = 0
            result = 0
            
            while True:
                b = ord(polyline_str[index]) - 63
                index += 1
                result |= (b & 0x1f) << shift
                shift += 5
                if b < 0x20:
                    break
            
            dlat = ~(result >> 1) if result & 1 else result >> 1
            lat += dlat
            
            shift = 0
            result = 0
            
            while True:
                b = ord(polyline_str[index]) - 63
                index += 1
                result |= (b & 0x1f) << shift
                shift += 5
                if b < 0x20:
                    break
            
            dlng = ~(result >> 1) if result & 1 else result >> 1
            lng += dlng
            
            coordinates.append((lat / 1e5, lng / 1e5))
        
        return coordinates
    
    def _extract_steps(self, steps):
        """Extract turn-by-turn directions from Google Maps steps"""
        directions = []
        
        for step in steps:
            direction = {
                'instruction': step.get('html_instructions', '').replace('<b>', '').replace('</b>', ''),
                'distance': step['distance']['value'] / 1000,  # km
                'duration': step['duration']['value'] / 60  # minutes
            }
            directions.append(direction)
        
        return directions
    
    def _extract_openroute_steps(self, segments):
        """Extract turn-by-turn directions from OpenRouteService segments"""
        directions = []
        
        for segment in segments:
            if 'steps' in segment:
                for step in segment['steps']:
                    direction = {
                        'instruction': step.get('instruction', 'Continue'),
                        'distance': step['distance'] / 1000,  # km
                        'duration': step['duration'] / 60  # minutes
                    }
                    directions.append(direction)
        
        return directions
    
    def get_multiple_routes(self, start_coords, end_coords, num_alternatives=3):
        """
        Get multiple alternative routes
        
        Args:
            start_coords: Start coordinates
            end_coords: End coordinates
            num_alternatives: Number of alternative routes to return
        
        Returns:
            list: List of route dictionaries
        """
        routes = []
        
        # Get primary route
        primary_route = self.get_optimal_route(start_coords, end_coords)
        if primary_route:
            routes.append(primary_route)
        
        # For simulation, generate alternatives with slight variations
        if primary_route and primary_route.get('simulated'):
            for i in range(1, num_alternatives):
                alt_route = primary_route.copy()
                # Vary distance and duration slightly
                alt_route['distance'] *= (1 + (i * 0.1))
                alt_route['duration'] *= (1 + (i * 0.15))
                alt_route['route_name'] = f"Alternative {i}"
                routes.append(alt_route)
        
        return routes
    
    def calculate_eta(self, route_data, current_time=None):
        """
        Calculate estimated time of arrival
        
        Args:
            route_data: Route dictionary from get_optimal_route
            current_time: Starting time (defaults to now)
        
        Returns:
            dict: ETA information
        """
        if current_time is None:
            current_time = datetime.now()
        
        # Use traffic-adjusted duration if available
        duration = route_data.get('duration_in_traffic', route_data.get('duration', 0))
        
        # Calculate ETA
        from datetime import timedelta
        eta = current_time + timedelta(minutes=duration)
        
        return {
            'eta': eta.isoformat(),
            'eta_formatted': eta.strftime('%Y-%m-%d %H:%M:%S'),
            'duration_minutes': duration,
            'distance_km': route_data.get('distance', 0)
        }
    
    def find_nearest_responder(self, emergency_coords, responder_locations):
        """
        Find the nearest emergency responder to an emergency location
        
        Args:
            emergency_coords: Emergency location (lat, lon)
            responder_locations: List of responder coordinates
        
        Returns:
            dict: Nearest responder info with route
        """
        nearest = None
        min_distance = float('inf')
        best_route = None
        
        for i, responder_coords in enumerate(responder_locations):
            route = self.get_optimal_route(responder_coords, emergency_coords)
            
            if route and route['distance'] < min_distance:
                min_distance = route['distance']
                nearest = {
                    'responder_id': i,
                    'coordinates': responder_coords,
                    'distance': route['distance'],
                    'duration': route['duration']
                }
                best_route = route
        
        if nearest:
            nearest['route'] = best_route
            nearest['eta'] = self.calculate_eta(best_route)
        
        return nearest

if __name__ == "__main__":
    # Test the Routing API
    routing_api = RoutingAPI(service='google')
    
    # Test locations
    start = (40.7589, -73.9851)  # Times Square, NYC
    end = (40.7128, -74.0060)    # Downtown NYC
    
    print("Testing Routing API...")
    print(f"\nStart: {start}")
    print(f"End: {end}")
    
    print("\nCalculating optimal route...")
    route = routing_api.get_optimal_route(start, end)
    
    if route:
        print(f"\nDistance: {route['distance']:.2f} km")
        print(f"Duration: {route['duration']:.1f} minutes")
        print(f"Number of waypoints: {len(route['coordinates'])}")
        
        # Calculate ETA
        eta_info = routing_api.calculate_eta(route)
        print(f"ETA: {eta_info['eta_formatted']}")
        
        # Test finding nearest responder
        print("\n\nTesting nearest responder finder...")
        responders = [
            (40.7500, -73.9900),
            (40.7300, -74.0100),
            (40.7700, -73.9700)
        ]
        
        nearest = routing_api.find_nearest_responder(end, responders)
        if nearest:
            print(f"Nearest responder: #{nearest['responder_id']}")
            print(f"Distance: {nearest['distance']:.2f} km")
            print(f"ETA: {nearest['eta']['eta_formatted']}")