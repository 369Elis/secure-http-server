import os
import re


import os
import re

# Reject path traversal and suspicious characters
def is_safe_path(base_dir, filename):
    # Block ../ or absolute paths
    if '..' in filename or filename.startswith('/') or '\\' in filename:
        return False
    # Normalize and ensure still within base directory
    normalized = os.path.normpath(os.path.join(base_dir, filename))
    return normalized.startswith(os.path.abspath(base_dir))

# Detect CRLF or %0d%0a in headers
def has_crlf_injection(request):
    return "%0d" in request.lower() or "%0a" in request.lower() 
