"""Compatibility facade; implementation lives in runner/adapters/persistence."""
from .models import *
from .adapters import *
from .adapters import _run_pymoo, _run_oade, _run_cgde, _run_sdr, _run_ce
from .persistence import *
from .runner import *

if __name__ == "__main__":
    main()
