"""
Browser Control Module
Handles browser automation with human-like mouse movements and interactions
"""

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout
import random
import math
from .human_behavior import HumanBehavior
from .config import SELECTORS, TIMING


class MouseController:
    """Controls mouse with human-like movements using Bezier curves"""
    
    def __init__(self, page: Page):
        self.page = page
        self.current_x = 500
        self.current_y = 500
    
    def bezier_curve(self, start_x, start_y, end_x, end_y):
        """Generate Bezier curve points for natural mouse movement"""
        # Random control points for curve
        ctrl1_x = start_x + random.uniform(-100, 100)
        ctrl1_y = start_y + random.uniform(-100, 100)
        ctrl2_x = end_x + random.uniform(-100, 100)
        ctrl2_y = end_y + random.uniform(-100, 100)
        
        points = []
        num_points = random.randint(15, 25)
        
        for i in range(num_points):
            t = i / (num_points - 1) if num_points > 1 else 1
            
            # Cubic Bezier curve formula
            x = ((1-t)**3 * start_x + 
                 3*(1-t)**2*t * ctrl1_x + 
                 3*(1-t)*t**2 * ctrl2_x + 
                 t**3 * end_x)
            
            y = ((1-t)**3 * start_y + 
                 3*(1-t)**2*t * ctrl1_y + 
                 3*(1-t)*t**2 * ctrl2_y + 
                 t**3 * end_y)
            
            points.append((int(x), int(y)))
        
        return points
    
    def move_to(self, x, y):
        """Move mouse naturally to target position"""
        points = self.bezier_curve(self.current_x, self.current_y, x, y)
        
        for i, (px, py) in enumerate(points):
            # Variable speed: slower at start/end, faster in middle
            if i < 3 or i > len(points) - 4:
                delay = random.uniform(0.020, 0.040)
            else:
                delay = random.uniform(0.005, 0.015)
            
            self.page.mouse.move(px, py)
            HumanBehavior.delay(int(delay * 1000), int(delay * 1000) + 5)
        
        self.current_x = x
        self.current_y = y
        HumanBehavior.hover_delay()
    
    def click_at(self, x, y):
        """Move to position and click naturally"""
        self.move_to(x, y)
        HumanBehavior.click_delay()
        
        # Click with natural duration
        self.page.mouse.down()
        HumanBehavior.delay(50, 120)
        self.page.mouse.up()
        HumanBehavior.delay(300, 600)


class BrowserController:
    """High-level browser control with human-like interactions"""
    
    def __init__(self, page: Page):
        self.page = page
        self.mouse = MouseController(page)
    
    def find_element(self, selectors, timeout=5000):
        """
        Try multiple selectors and return first visible element
        
        Args:
            selectors: List of selector strings or single selector
            timeout: Timeout per selector in ms
        
        Returns:
            Element or None
        """
        if isinstance(selectors, str):
            selectors = [selectors]
        
        for selector in selectors:
            try:
                element = self.page.wait_for_selector(selector, timeout=timeout)
                if element and element.is_visible():
                    return element
            except:
                continue
        
        return None
    
    def click_element(self, element):
        """Click an element with human-like behavior"""
        # Scroll into view if needed
        element.scroll_into_view_if_needed()
        HumanBehavior.delay(500, 1000)
        
        # Get bounding box
        box = element.bounding_box()
        if not box:
            # Fallback to direct click
            HumanBehavior.thinking_delay()
            element.click()
            return True
        
        # Calculate click position with random offset
        x_ratio, y_ratio = HumanBehavior.random_click_offset(box['width'], box['height'])
        x = int(box['x'] + box['width'] * x_ratio)
        y = int(box['y'] + box['height'] * y_ratio)
        
        # Move and click
        self.mouse.click_at(x, y)
        return True
    
    def simulate_reading_profile(self):
        """Simulate human reading a LinkedIn profile"""
        # Initial pause
        HumanBehavior.delay(*TIMING['reading'])
        
        # Scroll down to "read"
        scroll_amount = HumanBehavior.random_scroll_amount()
        self.page.mouse.wheel(0, scroll_amount)
        
        # Read more
        HumanBehavior.reading_delay()
        
        # Scroll back up
        self.page.mouse.wheel(0, -scroll_amount)
        HumanBehavior.delay(500, 1000)
    
    def type_like_human(self, text, typing_speed_wpm=None):
        """Type text with human-like speed and occasional pauses"""
        if typing_speed_wpm is None:
            typing_speed_wpm = HumanBehavior.typing_speed_wpm()
        
        chars_per_second = (typing_speed_wpm * 5) / 60
        
        for i, char in enumerate(text):
            # Variable speed
            base_delay = 1 / chars_per_second
            delay = base_delay * random.uniform(0.5, 1.5)
            
            # Occasional longer pauses (thinking)
            if random.random() < 0.05:
                HumanBehavior.thinking_delay()
            
            self.page.keyboard.press(char)
            HumanBehavior.delay(int(delay * 1000), int(delay * 1000) + 50)
        
        HumanBehavior.delay(300, 700)
    
    def search_person(self, name):
        """
        Search for a person on LinkedIn
        
        Args:
            name: Person's name to search
        
        Returns:
            True if search successful, False otherwise
        """
        try:
            # Find search box
            search_selectors = [
                'input.search-global-typeahead__input',
                'input[aria-label="Search"]',
                'input[placeholder="Search"]',
                'input[data-view-name="search-global-typeahead-input"]'
            ]
            
            search_box = self.find_element(search_selectors)
            if not search_box:
                return False
            
            # Click search box
            self.click_element(search_box)
            
            # Type the name
            self.type_like_human(name)
            
            # Press Enter
            self.page.keyboard.press("Enter")
            HumanBehavior.delay(*TIMING['page_load'])
            
            # Wait for results
            self.page.wait_for_load_state("networkidle")
            HumanBehavior.delay(1000, 2000)
            
            return True
            
        except Exception as e:
            print(f"   ❌ Search error: {e}")
            return False
    
    def click_first_person_result(self):
        """Click on the first person result from search"""
        try:
            # Selectors for person profile links
            person_selectors = [
                'a.app-aware-link[href*="/in/"]',
                'a[href*="/in/"].scale-down',
                '.entity-result__title-text a',
                'span.entity-result__title-text a'
            ]
            
            links = []
            for selector in person_selectors:
                try:
                    links = self.page.query_selector_all(selector)
                    if links:
                        break
                except:
                    continue
            
            if not links:
                return False
            
            # Click first result
            first_link = links[0]
            
            # Scroll to it
            first_link.scroll_into_view_if_needed()
            HumanBehavior.delay(800, 1500)
            
            # Simulate reading the result
            HumanBehavior.reading_delay(20)
            
            # Click
            self.click_element(first_link)
            
            # Wait for profile to load
            HumanBehavior.delay(*TIMING['page_load'])
            self.page.wait_for_load_state("networkidle")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Click result error: {e}")
            return False
    
    def download_cv_from_current_profile(self):
        """
        Download CV from the currently open profile
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Simulate reading the profile
            self.simulate_reading_profile()
            
            # Find "More" button
            more_button = self.find_element(SELECTORS['more_button'])
            if not more_button:
                print("   ❌ 'More' button not found")
                return False
            
            # Click "More"
            self.click_element(more_button)
            HumanBehavior.delay(*TIMING['menu_open'])
            
            # Find "Save to PDF"
            save_pdf = self.find_element(SELECTORS['save_to_pdf'])
            if not save_pdf:
                print("   ❌ 'Save to PDF' not found")
                return False
            
            # Click "Save to PDF"
            self.click_element(save_pdf)
            
            # Wait for PDF generation
            HumanBehavior.delay(*TIMING['pdf_generation'])
            
            return True
            
        except Exception as e:
            print(f"   ❌ Download error: {e}")
            return False
