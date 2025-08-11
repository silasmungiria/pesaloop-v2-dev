import logging
import requests
import user_agents
from ipware import get_client_ip
from ipaddress import ip_address as validate_ip
from django.conf import settings
from django.db import transaction
from django.core.cache import cache
from urllib.parse import urlparse

from tracking.utils import ActivityType


logger = logging.getLogger(__name__)

class ActivityTracker:
    """Comprehensive activity tracking with accurate geolocation and detailed logging."""

    CLOUD_PROVIDERS = [
        'aws', 'google', 'azure', 'cloudflare', 'digitalocean',
        'linode', 'heroku', 'rackspace', 'alibaba', 'oraclecloud'
    ]

    VPN_ASNS = ['AS60068', 'AS49666', 'AS60781']  # Example VPN ASNs
    TOR_EXIT_NODES_URL = "https://check.torproject.org/torbulkexitlist"

    def __init__(self, request, response=None, sensitive_fields=None):
        self.request = request
        self.response = response
        self.sensitive_fields = sensitive_fields or getattr(
            settings, 'ACTIVITY_TRACKING_SENSITIVE_FIELDS', ['password', 'token']
        )
        self.tor_exit_nodes = self._load_tor_exit_nodes()

    def _load_tor_exit_nodes(self):
        """Load and cache Tor exit nodes list."""
        cache_key = 'tor_exit_nodes'
        nodes = cache.get(cache_key)
        
        if nodes is None:
            try:
                response = requests.get(self.TOR_EXIT_NODES_URL, timeout=5)
                if response.status_code == 200:
                    nodes = set(response.text.splitlines())
                    cache.set(cache_key, nodes, 3600)  # Cache for 1 hour
                    logger.info(f"Loaded {len(nodes)} Tor exit nodes")
                else:
                    logger.warning(f"Failed to fetch Tor exit nodes: HTTP {response.status_code}")
                    nodes = set()
            except Exception as e:
                logger.error(f"Error loading Tor exit nodes: {str(e)}")
                nodes = set()
        return nodes

    def capture(self, activity_type=ActivityType.OTHER, **kwargs):
        """Main method to capture and store activity."""
        from ..models import Activity

        try:
            logger.info(f"Starting activity capture for type: {activity_type}")
            
            if activity_type not in ActivityType:
                logger.warning(f"Invalid activity type: {activity_type}, defaulting to OTHER")
                activity_type = ActivityType.OTHER

            data = {
                'type': activity_type,
                'user': self._get_user(),
                'session_id': self._get_session_id(),
                **self._get_network_data(),
                **self._get_geo_data(),
                **self._get_device_data(),
                **self._get_request_data(),
                **self._get_asn_data(),
                **kwargs
            }

            logger.debug(f"Activity data prepared: {self._sanitize_log_data(data)}")

            with transaction.atomic():
                activity = Activity(**data)
                activity.full_clean()
                activity.save()
                logger.info(f"Activity successfully saved with ID: {activity.id}")
                return activity

        except Exception as e:
            logger.error(f"Failed to capture activity: {str(e)}", exc_info=True)
            raise

    def _sanitize_log_data(self, data):
        """Sanitize sensitive data for logging."""
        sanitized = data.copy()
        if 'headers' in sanitized:
            sanitized['headers'] = {k: '*****' if k.lower() in ['authorization', 'cookie'] else v 
                                   for k, v in sanitized['headers'].items()}
        if 'params' in sanitized:
            sanitized['params'] = {k: '*****' if k.lower() in self.sensitive_fields else v 
                                  for k, v in sanitized['params'].items()}
        return sanitized

    def _get_user(self):
        """Get authenticated user."""
        try:
            if not hasattr(self.request, 'user'):
                logger.debug("Request has no user attribute")
                return None
                
            user = getattr(self.request, 'user', None)
            if user and user.is_authenticated:
                logger.debug(f"Authenticated user: {user.id}")
                return user
            logger.debug("No authenticated user found")
            return None
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None

    def _get_session_id(self):
        """Get session ID."""
        try:
            if not hasattr(self.request, 'session'):
                logger.debug("Request has no session attribute")
                return None
                
            session_key = getattr(self.request.session, 'session_key', None)
            logger.debug(f"Session ID: {'*****' if session_key else 'None'}")
            return session_key
        except Exception as e:
            logger.error(f"Error getting session ID: {str(e)}")
            return None

    def _get_network_data(self):
        """Get network data including IP address."""
        try:
            ip, is_routable = get_client_ip(self.request)
            if not ip:
                ip = '0.0.0.0'
                is_routable = False
                logger.warning("No IP address detected, using fallback")

            logger.info(f"Processing network data for IP: {ip}")
            
            network_data = {
                'ip_address': ip,
                'is_routable': is_routable,
                'is_cloud': self._is_cloud_ip(ip),
                'is_vpn': self._is_vpn_ip(ip),
                'is_tor': self._is_tor_exit_node(ip),
            }

            logger.debug(f"Network data collected: {network_data}")
            return network_data

        except Exception as e:
            logger.error(f"Failed to get network data: {str(e)}", exc_info=True)
            return {
                'ip_address': '0.0.0.0',
                'is_routable': False,
                'is_cloud': False,
                'is_vpn': False,
                'is_tor': False,
            }

    def _is_cloud_ip(self, ip):
        """Check if IP belongs to a cloud provider."""
        try:
            if not ip or ip == '0.0.0.0':
                return False

            try:
                hostname = validate_ip(ip).reverse_pointer
                logger.debug(f"Reverse DNS lookup for {ip}: {hostname}")
                
                is_cloud = any(
                    provider in hostname.lower()
                    for provider in self.CLOUD_PROVIDERS
                )
                
                if is_cloud:
                    logger.info(f"IP {ip} identified as cloud provider")
                return is_cloud
            except ValueError:
                logger.debug(f"IP {ip} is not valid for reverse lookup")
                return False
        except Exception as e:
            logger.error(f"Error checking cloud IP: {str(e)}")
            return False

    def _is_vpn_ip(self, ip):
        """Check if IP is from a VPN."""
        try:
            if not ip or ip == '0.0.0.0':
                return False

            asn_data = self._get_asn_data_for_ip(ip)
            if asn_data and asn_data.get('asn') in self.VPN_ASNS:
                logger.info(f"IP {ip} identified as VPN (ASN: {asn_data['asn']})")
                return True
            return False
        except Exception as e:
            logger.error(f"Error checking VPN IP: {str(e)}")
            return False

    def _is_tor_exit_node(self, ip):
        """Check if IP is a Tor exit node."""
        try:
            if not ip or ip == '0.0.0.0':
                return False

            if ip in self.tor_exit_nodes:
                logger.info(f"IP {ip} identified as Tor exit node")
                return True
            return False
        except Exception as e:
            logger.error(f"Error checking Tor exit node: {str(e)}")
            return False

    def _get_geo_data(self):
        """Get accurate geolocation data using ipinfo.io."""
        if getattr(settings, 'ACTIVITY_TRACKING_DISABLE_GEOLOCATION', False):
            logger.debug("Geolocation lookup disabled by settings")
            return {}

        ip_data = self._get_network_data()
        ip = ip_data['ip_address']
        
        if not ip or ip == '0.0.0.0':
            logger.debug("Skipping geolocation for invalid IP")
            return {}

        cache_key = f'geoip_{ip}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.debug(f"Using cached geolocation data for {ip}")
            return cached_data

        try:
            geo_data = self._get_geolocation(ip)
            if geo_data:
                cache.set(cache_key, geo_data, 86400)  # Cache for 1 day
                return geo_data
        except Exception as e:
            logger.error(f"Error getting geolocation data: {str(e)}")

        return {}

    def _get_geolocation(self, ip):
        """Accurate geolocation implementation using ipinfo.io."""
        logger.debug("Starting to fetching geolocation data")
        if not ip:
            return {}
        
        try:
            # url = f"https://ipinfo.io/{ip}/json"
            # if hasattr(settings, 'IPINFO_TOKEN'):
            #     url += f"?token={settings.IPINFO_TOKEN}"

            logger.debug(f"Fetching geolocation data from ipinfo.io for {ip}")
            # response = requests.get(url, timeout=2)
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=2)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Received geolocation data: {data}")
            
            return {
                "country": data.get("country", ""),
                "region": data.get("region", ""),
                "city": data.get("city", ""),
                "coordinates": data.get("loc", ""),
                "asn": data.get("org", "").split()[0] if data.get("org") else "",
                "isp": " ".join(data.get("org", "").split()[1:]) if data.get("org") else ""
            }
        except requests.RequestException as e:
            logger.error(f"Failed to get geolocation data from ipinfo.io: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error processing geolocation data: {str(e)}")
            return {}

    def _get_asn_data(self):
        """Get ASN/ISP information."""
        if getattr(settings, 'ACTIVITY_TRACKING_DISABLE_ASN_LOOKUP', False):
            logger.debug("ASN lookup disabled by settings")
            return {}

        ip_data = self._get_network_data()
        ip = ip_data['ip_address']

        if not ip or ip == '0.0.0.0':
            logger.debug("Skipping ASN lookup for invalid IP")
            return {}

        return self._get_asn_data_for_ip(ip)

    def _get_asn_data_for_ip(self, ip):
        """Get ASN data for specific IP."""
        cache_key = f'asn_{ip}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.debug(f"Using cached ASN data for {ip}")
            return cached_data

        try:
            # Try to get ASN from geo data first
            geo_data = self._get_geolocation(ip)
            if geo_data.get('asn'):
                asn_data = {
                    'asn': geo_data['asn'],
                    'isp': geo_data.get('isp', '')
                }
                cache.set(cache_key, asn_data, 86400)
                return asn_data

            # Fallback to ipapi.co if needed
            url = f"https://ipapi.co/{ip}/asn/"
            logger.debug(f"Fetching ASN data from ipapi.co for {ip}")
            response = requests.get(url, timeout=2)
            
            if response.status_code == 200:
                parts = response.text.strip().split(' ')
                asn_data = {
                    'asn': parts[0] if parts else '',
                    'isp': ' '.join(parts[1:]) if len(parts) > 1 else '',
                }
                logger.debug(f"ASN data retrieved: {asn_data}")
                cache.set(cache_key, asn_data, 86400)
                return asn_data
        except Exception as e:
            logger.error(f"Failed to get ASN data for {ip}: {str(e)}")

        return {}

    def _get_device_data(self):
        """Get comprehensive device information."""
        ua_string = self.request.META.get('HTTP_USER_AGENT', '')
        logger.debug(f"Processing user agent: {ua_string[:100]}...")
        
        try:
            ua = user_agents.parse(ua_string)
            device_data = {
                'device': ua.device.family if ua.device.family != 'Other' else '',
                'os': ua.os.family,
                'os_version': ua.os.version_string,
                'browser': ua.browser.family,
                'browser_version': ua.browser.version_string,
                'is_mobile': ua.is_mobile,
                'is_tablet': ua.is_tablet,
                'is_pc': ua.is_pc,
                'is_bot': ua.is_bot,
                'user_agent': ua_string,
            }
            logger.debug(f"Device data parsed: {device_data}")
            return device_data
        except Exception as e:
            logger.error(f"Failed to parse user agent: {str(e)}")
            return {
                'device': '',
                'os': '',
                'os_version': '',
                'browser': '',
                'browser_version': '',
                'is_mobile': None,
                'is_tablet': None,
                'is_pc': None,
                'is_bot': None,
                'user_agent': ua_string,
            }

    def _get_request_data(self):
        """Get comprehensive request data with sanitization."""
        request_data = {
            'endpoint': self._get_endpoint(),
            'method': self._get_method(),
            'status': self._get_status(),
            'duration': self._get_response_time(),
            'params': self._sanitize(self._get_params()) or {},
            'headers': self._sanitize_headers(dict(self.request.headers)),
            'referrer': self.request.META.get('HTTP_REFERER'),
        }
        logger.debug(f"Request data collected: {self._sanitize_log_data(request_data)}")
        return request_data

    def _get_endpoint(self):
        """Get request endpoint with validation."""
        endpoint = getattr(self.request, 'path', '')
        if not endpoint:
            logger.warning("No endpoint detected in request")
            return 'unknown'
        return endpoint[:255]

    def _get_method(self):
        """Get HTTP method with validation."""
        method = getattr(self.request, 'method', '').upper()
        if method not in {'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'}:
            logger.warning(f"Invalid HTTP method: {method}")
            return 'GET'
        return method

    def _get_status(self):
        """Get response status code."""
        if not self.response:
            logger.debug("No response object available for status code")
            return None
        try:
            return int(getattr(self.response, 'status_code', None))
        except (TypeError, ValueError) as e:
            logger.error(f"Invalid status code: {str(e)}")
            return None

    def _get_response_time(self):
        """Get response time in seconds."""
        if not self.response:
            logger.debug("No response object available for response time")
            return None
        try:
            duration = float(self.response.headers.get('X-Response-Time', 0))
            return max(0, duration)
        except (TypeError, ValueError) as e:
            logger.error(f"Invalid response time: {str(e)}")
            return None

    def _get_params(self):
        """Get request parameters with proper fallbacks."""
        if not hasattr(self.request, 'method'):
            logger.debug("Request has no method attribute")
            return {}

        method = self.request.method.upper()
        if method in ('GET', 'HEAD'):
            return getattr(self.request, 'GET', {}).dict()
        elif method in ('POST', 'PUT', 'PATCH'):
            if hasattr(self.request, 'data'):
                return self.request.data
            return getattr(self.request, 'POST', {}).dict()
        return {}

    def _sanitize(self, data):
        """Sanitize sensitive data in dictionaries."""
        if not isinstance(data, dict):
            return {}
        return {
            k: '*****' if k.lower() in [f.lower() for f in self.sensitive_fields] else v
            for k, v in data.items()
        }

    def _sanitize_headers(self, headers):
        """Sanitize sensitive headers."""
        if not isinstance(headers, dict):
            return {}
        sensitive_headers = ['authorization', 'cookie', 'set-cookie']
        return {
            k: '*****' if k.lower() in sensitive_headers else v
            for k, v in headers.items()
        }
