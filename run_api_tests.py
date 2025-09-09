import sys
import pytest

def main():
    # Run only tests marked with "api"
    retcode = pytest.main(["-m", "api", "-v", "--maxfail=1", "--disable-warnings"])
    sys.exit(retcode)

if __name__ == "__main__":
    main()
