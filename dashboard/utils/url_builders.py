#!/usr/bin/env python3
"""
URL Builders Utility - Clean URL Generation
Complementary URL building functions for component navigation.
"""

import re
from typing import Optional, Dict, Any, List
from urllib.parse import quote, urlencode

def sanitize_url_component(component: str) -> str:
    """Direct URL component sanitization"""
    if not component:
        return "unknown"

    sanitized = str(component).strip()
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '-', sanitized)
    sanitized = re.sub(r'-+', '-', sanitized)
    sanitized = sanitized.strip('-')

    return sanitized if sanitized else "unknown"

def build_facility_url(facility_id: str) -> str:
    """Build facility detail URL"""
    clean_id = sanitize_url_component(facility_id)
    return f"/facility/{clean_id}"

def build_analysis_url(analysis_type: str, target_id: Optional[str] = None) -> str:
    """Build analysis page URL"""
    clean_type = sanitize_url_component(analysis_type)

    if target_id:
        clean_target = sanitize_url_component(target_id)
        return f"/analysis/{clean_type}/{clean_target}"

    return f"/analysis/{clean_type}"

def build_detail_url(category: str, detail_type: str, params: Optional[Dict[str, Any]] = None) -> str:
    """Build detail page URL with parameters"""
    clean_category = sanitize_url_component(category)
    clean_type = sanitize_url_component(detail_type)

    base_url = f"/detail/{clean_category}/{clean_type}"

    if params:
        query_string = urlencode(params)
        return f"{base_url}?{query_string}"

    return base_url

def build_filter_url(base_path: str, filters: Dict[str, Any]) -> str:
    """Build filtered URL with query parameters"""
    if not filters:
        return base_path

    query_params = {key: str(value) for key, value in filters.items() if value is not None}

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
        return {'category': parts[0], 'detail_type': parts[1]}

    return None

def create_breadcrumb_data(pathname: str) -> List[Dict[str, str]]:
    """Generate breadcrumb navigation from URL"""
    breadcrumbs = [{'label': 'Portfolio Overview', 'url': '/'}]

    if not pathname or pathname == '/':
        return breadcrumbs

    if pathname.startswith('/facility/'):
        facility_id = parse_facility_url(pathname)
        if facility_id:
            breadcrumbs.append({
                'label': f'Facility: {facility_id}',
                'url': pathname
            })
    elif pathname.startswith('/detail/'):
        detail_data = parse_detail_url(pathname)
        if detail_data:
            breadcrumbs.extend([
                {'label': detail_data['category'].title(), 'url': f"/detail/{detail_data['category']}"},
                {'label': detail_data['detail_type'].title(), 'url': pathname}
            ])
    elif pathname.startswith('/workflow'):
        breadcrumbs.append({'label': 'Workflow Analysis', 'url': pathname})
    elif pathname.startswith('/data-quality'):
        breadcrumbs.append({'label': 'Data Quality', 'url': pathname})
    else:
        page_name = pathname.replace('/', '').replace('-', ' ').title()
        breadcrumbs.append({'label': page_name, 'url': pathname})

    return breadcrumbs

def get_navigation_context(pathname: str) -> Dict[str, Any]:
    """Get navigation context for current path"""
    context = {
        'current_page': 'portfolio',
        'facility_id': None,
        'detail_category': None,
        'breadcrumbs': create_breadcrumb_data(pathname)
    }

    if pathname and pathname.startswith('/facility/'):
        context['current_page'] = 'facility'
        context['facility_id'] = parse_facility_url(pathname)
    elif pathname and pathname.startswith('/detail/'):
        context['current_page'] = 'detail'
        detail_data = parse_detail_url(pathname)
        if detail_data:
            context['detail_category'] = detail_data['category']
    elif pathname and pathname.startswith('/workflow'):
        context['current_page'] = 'workflow'
    elif pathname and pathname.startswith('/data-quality'):
        context['current_page'] = 'data_quality'

    return context

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
        r'^/$',
        r'^/facility/.+$',
        r'^/detail/.+/.+$',
        r'^/workflow/?.*$',
        r'^/data-quality/?$',
        r'^/analysis/.+$'
    ]

    return any(re.match(pattern, pathname) for pattern in dashboard_patterns)

def get_page_title(pathname: str) -> str:
    """Get page title for current route"""
    title_mapping = {
        '/': 'Portfolio Overview',
        '/data-quality': 'Data Quality Foundation',
        '/workflow': 'Workflow Understanding',
        '/workflow-process': 'Workflow Process Analysis',
        '/summary': 'Four Facilities Summary',
        '/historical-records': 'Historical Records',
        '/facilities-distribution': 'Facilities Distribution',
        '/data-types-distribution': 'Data Types Distribution'
    }

    if pathname in title_mapping:
        return title_mapping[pathname]

    if pathname and pathname.startswith('/facility/'):
        facility_id = parse_facility_url(pathname)
        return f'{facility_id.title()} Facility Analysis' if facility_id else 'Facility Analysis'

    return 'Mining Reliability Database'