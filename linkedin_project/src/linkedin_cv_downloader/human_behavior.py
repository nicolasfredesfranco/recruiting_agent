"""
Human Behavior Simulation
Simulates natural human actions with realistic timing and randomness
"""

import time
import random


class HumanBehavior:
    """Simulates realistic human behavior patterns"""
    
    @staticmethod
    def delay(min_ms=300, max_ms=800):
        """Random delay to simulate thinking/reaction time"""
        time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))
    
    @staticmethod
    def reading_delay(text_length=100):
        """
        Simulate reading time based on text length
        Average reading speed: ~250 words per minute
        """
        words = text_length / 5  # Approximate words
        reading_time = (words / 4) + random.uniform(0.3, 0.8)
        time.sleep(min(reading_time, 3.0))  # Max 3 seconds
    
    @staticmethod
    def thinking_delay():
        """Pause as if thinking or deciding"""
        time.sleep(random.uniform(0.5, 1.2))
    
    @staticmethod
    def click_delay():
        """Natural pause before clicking"""
        time.sleep(random.uniform(0.2, 0.5))
    
    @staticmethod
    def hover_delay():
        """Brief pause while hovering over element"""
        time.sleep(random.uniform(0.1, 0.3))
    
    @staticmethod
    def random_scroll_amount():
        """Random scroll distance (pixels)"""
        return random.randint(250, 400)
    
    @staticmethod
    def mouse_movement_speed():
        """Random mouse movement speed multiplier"""
        return random.uniform(0.8, 1.3)
    
    @staticmethod
    def typing_speed_wpm():
        """Random typing speed in words per minute"""
        return random.randint(50, 80)
    
    @staticmethod
    def random_click_offset(width, height):
        """
        Random offset within element bounds to avoid always clicking center
        Returns: (x_ratio, y_ratio) between 0.0 and 1.0
        """
        x_ratio = random.uniform(0.3, 0.7)
        y_ratio = random.uniform(0.3, 0.7)
        return x_ratio, y_ratio
