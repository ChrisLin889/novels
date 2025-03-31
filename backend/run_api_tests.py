#!/usr/bin/env python3
"""
运行API集成测试脚本

这个脚本执行api_tests.py中的所有API集成测试。
"""

import sys
from api_tests import run_tests

if __name__ == '__main__':
    print("Running API integration tests...")
    success = run_tests()
    sys.exit(0 if success else 1) 