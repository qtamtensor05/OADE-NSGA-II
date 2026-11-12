"""Compatibility CLI; defaults to dry-run."""
import sys
from research.maintenance.tmp_sessions import main

if __name__ == "__main__":
    main(["clean", *sys.argv[1:]])
