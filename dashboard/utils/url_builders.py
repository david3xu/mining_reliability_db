#!/usr/bin/env python3
"""
URL Builders - Dynamic URL Generation Utilities
Clean URL management for dashboard navigation.
"""

import re
from typing import Optional, Dict, Any, List
from urllib.parse import quote, urlencode

def sanitize_url_component(component: str) -> str:
    """Sanitize component for URL safety"""
    if not component:
        return "unknown"

    # Convert to string and sanitize
    sanitized = str(component).strip()
    # Replace special characters with hyphens
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '-', sanitized)
    # Remove multiple consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')

    return sanitized if sanitized else "unknown"

def build_facility_url(facility_id: str) -> str:
    """Build facility detail URL"""
    sanitized_id = sanitize_url_component(facility_id)
    return f"/facility/{sanitized_id}"

def build_detail_url(category: str, detail_type: str, params: Optional[Dict[str, Any]] = None) -> str:
    """Build detail page URL with optional parameters"""
    sanitized_category = sanitize_url_component(category)
    sanitized_type = sanitize_url_component(detail_type)

    base_url = f"/detail/{sanitized_category}/{sanitized_type}"

    if params:
        query_string = urlencode(params)
        return f"{base_url}?{query_string}"

    return base_url

def build_analysis_url(analysis_type: str, target_id: Optional[str] = None) -> str:
    """Build analysis page URL"""
    sanitized_type = sanitize_url_component(analysis_type)

    if target_id:
        sanitized_target = sanitize_url_component(target_id)
        return f"/analysis/{sanitized_type}/{sanitized_target}"

    return f"/analysis/{sanitized_type}"

def build_filter_url(base_path: str, filters: Dict[str, Any]) -> str:
    """Build filtered URL with query parameters"""
    if not filters:
        return base_path

    query_params = {}
    for key, value in filters.items():
        if value is not None:
            query_params[key] = str(value)

    if query_params:
        query_string = urlencode(query_params)
        return f"{base_path}?{query_string}"

    return base_path

def parse_facility_url(pathname: str) -> Optional[str]:
    """Extract facility ID from URL path"""
    if not pathname or not pathname.startswith('/facility/'):
        return None

    facility_id = pathname.replace('/facility/', '')
    return facility_id if facility_id else None

def parse_detail_url(pathname: str) -> Optional[Dict[str, str]]:
    """Extract detail components from URL path"""
    if not pathname or not pathname.startswith('/detail/'):
        return None

    parts = pathname.replace('/detail/', '').split('/')

    if len(parts) >= 2:
        return {
            'category': parts[0],
            'detail_type': parts[1]
        }

    return None

def create_breadcrumb_data(pathname: str) -> List[Dict[str, str]]:
    """Generate breadcrumb navigation data from URL"""
    breadcrumbs = [{'label': 'Portfolio Overview', 'url': '/'}]

    if not pathname or pathname == '/':
        return breadcrumbs

    # Facility pages
    if pathname.startswith('/facility/'):
        facility_id = parse_facility_url(pathname)
        if facility_id:
            breadcrumbs.append({
                'label': f'Facility: {facility_id}',
                'url': pathname
            })

    # Detail pages
    elif pathname.startswith('/detail/'):
        detail_data = parse_detail_url(pathname)
        if detail_data:
            breadcrumbs.extend([
                {'label': detail_data['category'].title(), 'url': f"/detail/{detail_data['category']}"},
                {'label': detail_data['detail_type'].title(), 'url': pathname}
            ])

    # Network analysis
    elif pathname.startswith('/network'):
        breadcrumbs.append({'label': 'Network Analysis', 'url': '/network'})

    return breadcrumbs

def get_navigation_context(pathname: str) -> Dict[str, Any]:
    """Get navigation context for current path"""
    context = {
        'current_page': 'portfolio',
        'facility_id': None,
        'detail_category': None,
        'breadcrumbs': create_breadcrumb_data(pathname)
    }

    if pathname.startswith('/facility/'):
        context['current_page'] = 'facility'
        context['facility_id'] = parse_facility_url(pathname)

    elif pathname.startswith('/detail/'):
        context['current_page'] = 'detail'
        detail_data = parse_detail_url(pathname)
        if detail_data:
            context['detail_category'] = detail_data['category']

    elif pathname.startswith('/network'):
        context['current_page'] = 'network'

    return context

# URL validation utilities
def is_valid_facility_url(pathname: str) -> bool:
    """Validate facility URL format"""
    if not pathname or not pathname.startswith('/facility/'):
        return False

    facility_id = parse_facility_url(pathname)
    return bool(facility_id and len(facility_id) > 0)

def is_dashboard_url(pathname: str) -> bool:
    """Check if URL is within dashboard scope"""
    if not pathname:
        return False

    dashboard_patterns = [
        r'^/$',  # Home
        r'^/facility/.+$',  # Facility pages
        r'^/detail/.+/.+$',  # Detail pages
        r'^/network/?$',  # Network analysis
        r'^/analysis/.+$'  # Analysis pages
    ]

    return any(re.match(pattern, pathname) for pattern in dashboard_patterns)
