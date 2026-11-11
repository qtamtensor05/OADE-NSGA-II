from __future__ import annotations

import copy
import unittest
import uuid
from contextlib import contextmanager
from pathlib import Path

from src.benchmarking.algorithm_benchmark import AlgorithmSpec
from src.benchmarking.provenance import (
    assert_compatible, checkpoint_manifest, prepare_manifest, validate_records, PRIMARY_FILES,
)


@contextmanager
def evidence_directory():
    # Ordinary inherited ACLs keep this usable inside Windows app sandboxes.
    root = Path(__file__).resolve().parents[1] / "scratch"
    directory = root / f"test-provenance-{uuid.uuid4().hex}"
    directory.mkdir(parents=True)
    try:
        yield directory
    finally:
        for path in directory.iterdir():
            path.unlink()
        directory.rmdir()


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.cfg = {"global": {"runs": 1, "evaluation_budget": 100, "seed_base": 42},
                    "problems": [{"name": "zdt1", "n_var": 3}]}
        self.specs = [AlgorithmSpec("OADE", "local_oade", {})]
        self.raw = [{"problem": "zdt1", "algorithm": "OADE", "runner": "local_oade",
                     "run_idx": 0, "seed": 42, "n_var": 3, "n_obj": 2,
                     "evaluation_budget": 100, "n_eval": 100, "front_size": 10,
                     "valid": True, "validation_status": "ok", "IGD": 0.1, "HV": 0.5}]
        self.validation = copy.deepcopy(self.raw)
        self.manifest = {"schema": 1, "kind": "captured_before_execution", "protocol": {},
                         "source_hashes": {}, "environment": {}, "artifacts": {}}

    def test_missing_duplicate_or_wrong_seed_cannot_be_reused(self):
        for rows in ([], self.raw * 2, [dict(self.raw[0], seed=43)]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                validate_records(rows, self.validation, self.cfg, self.specs, require_complete=True)

    def test_valid_raw_requires_matching_validation(self):
        validate_records(self.raw, self.validation, self.cfg, self.specs, require_complete=True)
        with self.assertRaises(ValueError):
            validate_records(self.raw, [], self.cfg, self.specs)
        with self.assertRaises(ValueError):
            validate_records(self.raw, [dict(self.validation[0], n_eval=99)], self.cfg, self.specs)

    def test_invalid_metrics_remain_valid_evidence_records(self):
        raw = [dict(self.raw[0], valid=False, validation_status="collapsed_front", IGD=float("nan"))]
        validate_records(raw, copy.deepcopy(raw), self.cfg, self.specs, require_complete=True)

    def test_partial_problem_rejected_even_when_total_count_looks_complete(self):
        cfg = copy.deepcopy(self.cfg)
        cfg["global"]["runs"] = 2
        with self.assertRaises(ValueError):
            validate_records(self.raw, self.validation, cfg, self.specs)

    def test_manifest_rejects_environment_config_source_and_historical_drift(self):
        assert_compatible(self.manifest, copy.deepcopy(self.manifest))
        for key in ("protocol", "source_hashes", "environment"):
            changed = copy.deepcopy(self.manifest)
            changed[key] = {"changed": True}
            with self.subTest(key=key), self.assertRaises(ValueError):
                assert_compatible(self.manifest, changed)
        with self.assertRaises(ValueError):
            assert_compatible(dict(self.manifest, kind="historical_inventory"), self.manifest)

    def test_existing_evidence_is_never_overwritten_and_tamper_blocks_resume(self):
        with evidence_directory() as directory:
            out = Path(directory)
            manifest = prepare_manifest(out, copy.deepcopy(self.manifest))
            for name in PRIMARY_FILES:
                (out / name).write_text("checkpoint", encoding="utf-8")
            checkpoint_manifest(out, manifest)
            prepare_manifest(out, self.manifest, resume=True)
            with self.assertRaises(ValueError):
                prepare_manifest(out, self.manifest)
            (out / PRIMARY_FILES[0]).write_text("tampered", encoding="utf-8")
            with self.assertRaises(ValueError):
                prepare_manifest(out, self.manifest, resume=True)

    def test_missing_execution_manifest_rejected_for_historical_csv(self):
        with evidence_directory() as directory:
            out = Path(directory)
            (out / PRIMARY_FILES[0]).write_text("historical", encoding="utf-8")
            with self.assertRaises(ValueError):
                prepare_manifest(out, self.manifest, resume=True)


if __name__ == "__main__":
    unittest.main()
