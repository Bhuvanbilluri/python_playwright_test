from playwright.sync_api import sync_playwright

from ab_testing import test_ab_testing
from add_remove_elements import test_add_remove_elements
from basic_auth import test_basic_auth
from broken_images import test_broken_images

tests = [
    test_ab_testing,
    test_add_remove_elements,
    test_basic_auth,
    # test_broken_images
]

def run_all_tests():
    passed = 0
    failed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for test in tests:
            try:
                print(f"Running {test.__name__}")
                test(page)
                print(f"{test.__name__} ✅ PASSED\n")
                passed += 1
            except Exception as e:
                print(f"{test.__name__} ❌ FAILED")
                print(f"Error: {e}\n")
                failed += 1

        browser.close()

    # Final Summary
    print("=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

run_all_tests()