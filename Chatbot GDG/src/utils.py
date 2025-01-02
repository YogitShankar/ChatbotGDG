import os
import platform
import stat
from shutil import which, move
import webbrowser
import configparser

def setup_chromedriver():
    """Setup ChromeDriver with correct permissions in the project directory"""
    config = configparser.ConfigParser()
    config.read('/Users/ayushagarwal/Documents/Python/config/config.ini')
    driver_path_config = config['DEFAULT'].get('driver_path', '')

    if driver_path_config and os.path.isfile(driver_path_config):
        st = os.stat(driver_path_config)
        os.chmod(driver_path_config, st.st_mode | stat.S_IEXEC)
        return driver_path_config

    project_root = os.path.dirname(os.path.dirname(__file__))
    drivers_dir = os.path.join(project_root, 'drivers')
    os.makedirs(drivers_dir, exist_ok=True)
    
    chromedriver = "chromedriver"
    if platform.system() == "Windows":
        chromedriver += ".exe"
    
    # First check project locations
    project_locations = [
        os.path.join(project_root, chromedriver),  # Root directory
        os.path.join(drivers_dir, chromedriver),   # Drivers directory
    ]
    
    # Look for ChromeDriver in project locations
    for location in project_locations:
        if os.path.isfile(location):
            # Make ChromeDriver executable
            st = os.stat(location)
            os.chmod(location, st.st_mode | stat.S_IEXEC)
            return location
            
    # If ChromeDriver is in current directory but not in project structure
    if os.path.isfile("./chromedriver"):
        # Move it to drivers directory
        dest_path = os.path.join(drivers_dir, chromedriver)
        move("./chromedriver", dest_path)
        # Make it executable
        st = os.stat(dest_path)
        os.chmod(dest_path, st.st_mode | stat.S_IEXEC)
        return dest_path
    
    raise ValueError(
        f"\nPlease place chromedriver in one of these locations:\n"
        f"1. {project_locations[0]}\n"
        f"2. {project_locations[1]}"
    )

def get_chromedriver_path():
    """Find and setup ChromeDriver"""
    try:
        return setup_chromedriver()
    except ValueError as e:
        print(e)
        print("\nMake sure to:")
        print("1. Download ChromeDriver matching your Chrome version")
        print("2. Extract the downloaded file")
        print("3. Place it in one of the locations above")
        print("4. Make sure it has execute permissions")
        raise
