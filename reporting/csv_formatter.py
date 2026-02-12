#!/usr/bin/env python3
"""
CSV formatting for workflow data with schema support.

This module handles converting JSON workflow data to CSV format based on
schema definitions that specify field mappings, types, and denormalization.
"""

import csv
import io
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


def load_schema(schema_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load a YAML schema file.
    
    Args:
        schema_path: Path to YAML schema file
        
    Returns:
        Parsed schema dict, or None on error
    """
    try:
        with open(schema_path, 'r') as f:
            schemas = yaml.safe_load(f)
            # Return first schema in file
            if schemas:
                return list(schemas.values())[0]
            return None
    except FileNotFoundError:
        print(f"Error: Schema file not found: {schema_path}", file=sys.stderr)
        return None
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in schema: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error loading schema: {e}", file=sys.stderr)
        return None


def _get_nested_value(data: Dict[str, Any], path: str) -> Any:
    """
    Get value from nested dict using dot notation.
    
    Args:
        data: Source dictionary
        path: Dot-separated path (e.g., 'actor.login')
        
    Returns:
        Value at path, or None if not found
    """
    parts = path.split('.')
    current = data
    
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    
    return current


def _format_value(value: Any, field_type: str, format_spec: Optional[str] = None) -> str:
    """
    Format a value according to its type specification.
    
    Args:
        value: Value to format
        field_type: Type specification (string, integer, timestamp, etc.)
        format_spec: Optional format string for timestamps
        
    Returns:
        Formatted string value
    """
    if value is None:
        return ''
    
    if field_type == 'integer':
        try:
            return str(int(value))
        except (ValueError, TypeError):
            return ''
    
    elif field_type == 'float':
        try:
            return str(float(value))
        except (ValueError, TypeError):
            return ''
    
    elif field_type == 'boolean':
        if isinstance(value, bool):
            return 'true' if value else 'false'
        return str(value).lower()
    
    elif field_type == 'timestamp':
        if not value:
            return ''
        try:
            # Parse ISO format timestamp
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            if format_spec:
                return dt.strftime(format_spec)
            return value
        except (ValueError, AttributeError):
            return str(value)
    
    elif field_type == 'url':
        return str(value) if value else ''
    
    else:  # string or unknown
        return str(value)


def _expand_array(data: Dict[str, Any], expand_field: str) -> List[Dict[str, Any]]:
    """
    Expand an array field into multiple rows (denormalization).
    
    Args:
        data: Source dictionary
        expand_field: Field name containing array to expand
        
    Returns:
        List of dicts, one per array item, with parent data included
    """
    array_data = _get_nested_value(data, expand_field)
    
    if not array_data or not isinstance(array_data, list):
        # No array to expand, return single row
        return [data]
    
    # Create one row per array item, with parent data repeated
    expanded = []
    for item in array_data:
        row_data = data.copy()
        # Add array item data with array prefix
        row_data[expand_field] = item
        expanded.append(row_data)
    
    return expanded


def format_as_csv(
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    schema: Dict[str, Any]
) -> str:
    """
    Format data as CSV according to schema.
    
    Args:
        data: Source data (dict or list of dicts)
        schema: Schema definition with fields and format settings
        
    Returns:
        CSV-formatted string
        
    Example:
        >>> schema = {
        ...     'mode': 'denormalized',
        ...     'fields': [
        ...         {'source': 'id', 'column': 'run_id', 'type': 'integer'},
        ...         {'source': 'name', 'column': 'workflow', 'type': 'string'}
        ...     ]
        ... }
        >>> data = {'id': 123, 'name': 'test'}
        >>> csv_output = format_as_csv(data, schema)
    """
    # Normalize data to list
    if isinstance(data, dict):
        data_list = [data]
    else:
        data_list = data
    
    if not data_list:
        return ''
    
    fields = schema.get('fields', [])
    if not fields:
        return ''
    
    # Extract column names
    columns = [f['column'] for f in fields]
    
    # Prepare CSV output
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(columns)
    
    # Check if we need to expand arrays
    expand_field = schema.get('expand')
    
    # Process each data item
    for item in data_list:
        # Expand arrays if specified
        if expand_field:
            expanded_items = _expand_array(item, expand_field)
        else:
            expanded_items = [item]
        
        # Write row for each expanded item
        for expanded_item in expanded_items:
            row = []
            for field in fields:
                source = field['source']
                field_type = field.get('type', 'string')
                format_spec = field.get('format')
                
                # Get value from source path
                value = _get_nested_value(expanded_item, source)
                
                # Format according to type
                formatted = _format_value(value, field_type, format_spec)
                row.append(formatted)
            
            writer.writerow(row)
    
    return output.getvalue()


def save_csv(
    csv_content: str,
    output_path: Path,
    append: bool = False
) -> bool:
    """
    Save CSV content to file.
    
    Args:
        csv_content: CSV-formatted string
        output_path: Path to output file
        append: If True, append to existing file (skip header if file exists)
        
    Returns:
        True if successful, False on error
    """
    try:
        mode = 'a' if append and output_path.exists() else 'w'
        
        # If appending and file exists, skip the header line
        content_to_write = csv_content
        if mode == 'a' and output_path.exists() and output_path.stat().st_size > 0:
            # Skip first line (header)
            lines = csv_content.split('\n', 1)
            if len(lines) > 1:
                content_to_write = lines[1]
        
        with open(output_path, mode) as f:
            f.write(content_to_write)
        
        return True
    except Exception as e:
        print(f"Error saving CSV: {e}", file=sys.stderr)
        return False
