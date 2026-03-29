import sys
import os

# Thêm đường dẫn để import được module protocol
# Vì file test nằm trong Code/test/, cần lên 2 cấp để đến thư mục Code
# Code/test/test_message.py -> Code/ -> thêm vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import từ protocol
from protocol.message import (
    build_join,
    build_message,
    build_leave,
    encode_message,
    decode_message,
    MSG_JOIN,
    MSG_MSG,
    MSG_LEAVE,
    SEPARATOR,
    DELIMITER
)


# =============================================================================
# TEST FUNCTIONS (không cần pytest)
# =============================================================================

def run_tests():
    """Chạy tất cả test mà không cần pytest"""
    tests = [
        ("Test build_join simple", test_build_join_simple),
        ("Test build_join unicode", test_build_join_unicode),
        ("Test build_message simple", test_build_message_simple),
        ("Test build_message with separator", test_build_message_with_separator),
        ("Test build_leave", test_build_leave),
        ("Test encode JOIN", test_encode_join),
        ("Test encode MSG", test_encode_msg),
        ("Test decode JOIN", test_decode_join),
        ("Test decode MSG", test_decode_msg),
        ("Test decode LEAVE", test_decode_leave),
        ("Test decode invalid", test_decode_invalid),
        ("Test integration JOIN flow", test_integration_join),
        ("Test integration MSG flow", test_integration_msg),
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("RUNNING MESSAGE PROTOCOL TESTS")
    print("=" * 60)
    
    for test_name, test_func in tests:
        try:
            test_func()
            print(f"✓ PASS: {test_name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ FAIL: {test_name}")
            print(f"  Reason: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {test_name}")
            print(f"  Exception: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


# =============================================================================
# TEST CASES
# =============================================================================

def test_build_join_simple():
    result = build_join("Alice")
    assert result == "JOIN|Alice", f"Expected 'JOIN|Alice', got '{result}'"


def test_build_join_unicode():
    result = build_join("Nguyễn Văn A")
    assert result == "JOIN|Nguyễn Văn A", f"Expected 'JOIN|Nguyễn Văn A', got '{result}'"


def test_build_message_simple():
    result = build_message("Alice", "Hello")
    assert result == "MSG|Alice|Hello", f"Expected 'MSG|Alice|Hello', got '{result}'"


def test_build_message_with_separator():
    result = build_message("Bob", "Hello | World")
    assert result == "MSG|Bob|Hello | World", f"Expected 'MSG|Bob|Hello | World', got '{result}'"


def test_build_leave():
    result = build_leave("Alice")
    assert result == "LEAVE|Alice", f"Expected 'LEAVE|Alice', got '{result}'"


def test_encode_join():
    result = encode_message("JOIN|Alice")
    assert result == b"JOIN|Alice\n", f"Expected b'JOIN|Alice\\n', got {result}"


def test_encode_msg():
    result = encode_message("MSG|Bob|Hello")
    assert result == b"MSG|Bob|Hello\n", f"Expected b'MSG|Bob|Hello\\n', got {result}"


def test_decode_join():
    result = decode_message("JOIN|Alice")
    expected = {"type": "JOIN", "username": "Alice"}
    assert result == expected, f"Expected {expected}, got {result}"


def test_decode_msg():
    result = decode_message("MSG|Alice|Hello World")
    expected = {"type": "MSG", "username": "Alice", "text": "Hello World"}
    assert result == expected, f"Expected {expected}, got {result}"


def test_decode_leave():
    result = decode_message("LEAVE|Alice")
    expected = {"type": "LEAVE", "username": "Alice"}
    assert result == expected, f"Expected {expected}, got {result}"


def test_decode_invalid():
    result = decode_message("UNKNOWN|data")
    assert result["type"] == "UNKNOWN", f"Expected type UNKNOWN, got {result['type']}"
    assert result["raw"] == "UNKNOWN|data", f"Expected raw 'UNKNOWN|data', got {result['raw']}"


def test_integration_join():
    original = build_join("Alice")
    encoded = encode_message(original)
    decoded = decode_message(encoded.decode('utf-8').strip())
    expected = {"type": "JOIN", "username": "Alice"}
    assert decoded == expected, f"Integration failed: {decoded} != {expected}"


def test_integration_msg():
    original = build_message("Bob", "Hello | World!")
    encoded = encode_message(original)
    decoded = decode_message(encoded.decode('utf-8').strip())
    expected = {"type": "MSG", "username": "Bob", "text": "Hello | World!"}
    assert decoded == expected, f"Integration failed: {decoded} != {expected}"


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
