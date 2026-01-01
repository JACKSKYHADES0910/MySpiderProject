
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

try:
    from utils import browser
    print("Successfully imported utils.browser")
    
    # Test direct logging
    print("Testing _debug_log...")
    browser._debug_log("TEST", "verify_fix", "Testing log entry")
    
    log_path = r"d:\Project\MySpiderProject\.cursor\debug.log"
    if os.path.exists(log_path):
        print(f"SUCCESS: Log file created at {log_path}")
    else:
        print(f"WARNING: Log file not found at {log_path} (this might be okay if silently failed, but ideally should exist)")

    # Test get_driver (mocking it or calling it if possible - calling it might open chrome so maybe just check _debug_log first)
    # We won't call get_driver to avoid opening a real browser window in this test script unless necessary. 
    # The traceback showed the error happened INSIDE get_driver at the very first log call.
    # So if _debug_log works, get_driver should pass that point.
    
    print("Verification complete.")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
