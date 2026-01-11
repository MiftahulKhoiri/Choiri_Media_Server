"""
cms_errors.py
Custom exception untuk CMS
"""


class CMSError(Exception):
    """
    Base exception untuk seluruh CMS
    """
    pass


class CMSBootstrapError(CMSError):
    """
    Error saat proses bootstrap sistem
    """
    pass


class CMSDependencyError(CMSError):
    """
    Error dependency (Git, pip, dll)
    """
    pass


class CMSVirtualEnvError(CMSError):
    """
    Error terkait virtual environment
    """
    pass


class CMSPermissionError(CMSError):
    """
    Error hak akses (root / permission)
    """
    pass


class CMSConfigError(CMSError):
    """
    Error konfigurasi / env
    """
    pass