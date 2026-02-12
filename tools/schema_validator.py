#!/usr/bin/env python3
"""
JSON Schema validation utilities for front matter validation.

This module provides schema validation functionality for validating YAML front matter
in markdown files against JSON schemas. It includes schema caching and intelligent
error categorization (required vs optional field errors).

Usage:
    from schema_validator import validate_front_matter_schema
    
    is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        metadata=metadata,
        schema_path="path/to/schema.json",
        file_path="file.md",
        use_actions=True,
        action_level="warning"
    )
"""

import json
from pathlib import Path
from typing import Optional, Dict, Tuple, List, Any

from doc_test_utils import log, HELP_URLS

# Try to import jsonschema
try:
    import jsonschema
    from jsonschema import Draft7Validator
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

# Default schema path for front matter validation
DEFAULT_SCHEMA_PATH = '.github/schemas/front-matter-schema.json'

# Schema cache - stores loaded schemas to avoid repeated file I/O
_SCHEMA_CACHE: Dict[str, Dict[str, Any]] = {}


def clear_schema_cache() -> None:
    """
    Clear the schema cache.
    
    Useful for testing or when schemas are modified at runtime.
    """
    global _SCHEMA_CACHE
    _SCHEMA_CACHE.clear()


def load_schema(schema_path: str) -> Optional[Dict[str, Any]]:
    """
    Load a JSON schema from file with caching.
    
    Args:
        schema_path: Path to JSON schema file
        
    Returns:
        Schema dictionary, or None if loading fails
        
    Example:
        >>> schema = load_schema('.github/schemas/front-matter-schema.json')
        >>> if schema:
        ...     required_fields = schema.get('required', [])
        ...     print(f"Schema has {len(required_fields)} required fields")
        
    Note:
        Schemas are cached after first load. Use clear_schema_cache()
        to force reload.
    """
    # Check cache first
    if schema_path in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[schema_path]
    
    # Load from file
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        # Cache for future use
        _SCHEMA_CACHE[schema_path] = schema
        return schema
        
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
    except Exception:
        return None


def categorize_validation_error(error: Any, schema: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Categorize a jsonschema validation error as critical (required field) or warning (optional field).
    
    Args:
        error: A jsonschema ValidationError
        schema: The JSON schema being validated against
        
    Returns:
        Tuple of (is_required_error, error_message)
        
    Example:
        >>> from jsonschema import Draft7Validator
        >>> schema = {'type': 'object', 'required': ['name']}
        >>> validator = Draft7Validator(schema)
        >>> errors = list(validator.iter_errors({'age': 25}))
        >>> is_required, msg = categorize_validation_error(errors[0], schema)
        >>> print(f"Required: {is_required}, Message: {msg}")
        Required: True, Message: Required field missing: name
        
    Note:
        Required field errors are critical and should fail validation.
        Optional field errors are warnings that don't fail validation.
    """
    is_required = False
    
    # Check if error is about a required property
    if error.validator == 'required':
        is_required = True
        missing_field = error.message.split("'")[1] if "'" in error.message else "unknown"
        message = f"Required field missing: {missing_field}"
        return is_required, message
    
    # Check if error is about an enum value
    if error.validator == 'enum' and len(error.absolute_path) > 0:
        field_name = '.'.join(str(p) for p in error.absolute_path)
        # Check if this field is in the required list
        if error.absolute_path[0] in schema.get('required', []):
            is_required = True
            message = f"Invalid value for required field '{field_name}': {error.message}"
        else:
            message = f"Invalid value for optional field '{field_name}': {error.message}"
        return is_required, message
    
    # Check if error is about type or format
    if error.validator in ['type', 'format', 'pattern', 'minimum', 'maximum', 'minLength', 'maxLength']:
        field_name = '.'.join(str(p) for p in error.absolute_path)
        # Check if this field is in the required list
        if len(error.absolute_path) > 0 and error.absolute_path[0] in schema.get('required', []):
            is_required = True
            message = f"Invalid format for required field '{field_name}': {error.message}"
        else:
            message = f"Invalid format for optional field '{field_name}': {error.message}"
        return is_required, message
    
    # Other errors default to warnings for optional fields
    field_name = '.'.join(str(p) for p in error.absolute_path) if error.absolute_path else "unknown"
    message = f"Validation issue in '{field_name}': {error.message}"
    return is_required, message


def validate_front_matter_schema(
    metadata: Dict[str, Any],
    schema_path: str,
    file_path: Optional[str] = None,
    use_actions: bool = False,
    action_level: str = "warning"
) -> Tuple[bool, bool, List[str], List[str]]:
    """
    Validate front matter metadata against a JSON schema.
    
    This function validates YAML front matter (parsed as a dictionary) against
    a JSON schema. It distinguishes between errors in required fields (critical)
    and errors in optional fields (warnings).
    
    Args:
        metadata: Parsed front matter dictionary
        schema_path: Path to JSON schema file
        file_path: Optional path to markdown file (for logging)
        use_actions: Whether to output GitHub Actions annotations
        action_level: Annotation level filter (all, warning, error)
        
    Returns:
        Tuple of (is_valid, has_warnings, error_messages, warning_messages)
        - is_valid: True if no required field errors
        - has_warnings: True if any warnings (optional field issues)
        - error_messages: List of error strings
        - warning_messages: List of warning strings
        
    Example:
        >>> metadata = {'layout': 'default', 'title': 'Test'}
        >>> is_valid, has_warnings, errors, warnings = validate_front_matter_schema(
        ...     metadata, 'schema.json', 'test.md'
        ... )
        >>> if not is_valid:
        ...     print(f"Validation failed: {errors}")
        ... elif has_warnings:
        ...     print(f"Validation warnings: {warnings}")
        
    Note:
        If jsonschema library is not installed, validation is skipped with a warning.
        Schema files are cached after first load for performance.
    """
    # Check if jsonschema is available
    if not JSONSCHEMA_AVAILABLE:
        log("jsonschema library not installed; run: pip install jsonschema", 
            "warning", file_path, None, use_actions, action_level)
        return True, False, [], []
    
    # Load schema (with caching)
    schema = load_schema(schema_path)
    
    if schema is None:
        # Check which error occurred
        try:
            with open(schema_path, 'r') as f:
                json.load(f)
        except FileNotFoundError:
            log(f"Schema file not found: {schema_path}", 
                "warning", file_path, None, use_actions, action_level)
            return True, False, [], []
        except json.JSONDecodeError as e:
            log(f"Invalid JSON schema: {str(e)}", 
                "warning", file_path, None, use_actions, action_level)
            return True, False, [], []
        except Exception as e:
            log(f"Error loading schema: {str(e)}", 
                "warning", file_path, None, use_actions, action_level)
            return True, False, [], []
    
    # At this point, schema is guaranteed to be a Dict (not None)
    # Type checkers need help understanding this
    assert schema is not None
    
    # Create validator
    validator = Draft7Validator(schema)
    errors: List[str] = []
    warnings: List[str] = []
    
    # Collect all validation errors
    for error in validator.iter_errors(metadata):
        is_required, message = categorize_validation_error(error, schema)
        
        if is_required:
            errors.append(message)
        else:
            warnings.append(message)
    
    # Report errors
    if errors:
        log("Front matter validation errors found:", "error", file_path, None, use_actions, action_level)
        for error_msg in errors:
            log(f"  - {error_msg}", "error", file_path, None, use_actions, action_level)
        log(f"-  Help: {HELP_URLS['front_matter']}", "info")
    
    # Report warnings
    if warnings:
        log("Front matter validation warnings:", "warning", file_path, None, use_actions, action_level)
        for warning_msg in warnings:
            log(f"  - {warning_msg}", "warning", file_path, None, use_actions, action_level)
    
    if not errors and not warnings:
        log("Front matter validation passed", "success")
    
    return len(errors) == 0, len(warnings) > 0, errors, warnings


def validate_with_default_schema(
    metadata: Dict[str, Any],
    file_path: Optional[str] = None,
    use_actions: bool = False,
    action_level: str = "warning"
) -> Tuple[bool, bool, List[str], List[str]]:
    """
    Validate front matter using the default schema location.
    
    This is a convenience function that uses the standard schema path
    defined in DEFAULT_SCHEMA_PATH constant.
    
    Args:
        metadata: Parsed front matter dictionary
        file_path: Optional path to markdown file (for logging)
        use_actions: Whether to output GitHub Actions annotations
        action_level: Annotation level filter (all, warning, error)
        
    Returns:
        Tuple of (is_valid, has_warnings, error_messages, warning_messages)
        
    Example:
        >>> metadata = {'layout': 'default', 'title': 'Test', 'description': 'A test page'}
        >>> is_valid, _, _, _ = validate_with_default_schema(metadata)
        >>> if is_valid:
        ...     print("Front matter is valid")
    """
    return validate_front_matter_schema(
        metadata=metadata,
        schema_path=DEFAULT_SCHEMA_PATH,
        file_path=file_path,
        use_actions=use_actions,
        action_level=action_level
    )
