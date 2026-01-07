"""
LinkedIn CV Downloader
Automated CV downloading from LinkedIn with human-like behavior simulation
"""

__version__ = "1.0.0"
__author__ = "Nicolas Fredes"

from .cv_downloader import LinkedInCVDownloader
from .human_behavior import HumanBehavior
from .browser_control import BrowserController

__all__ = [
    'LinkedInCVDownloader',
    'HumanBehavior',
    'BrowserController',
]
