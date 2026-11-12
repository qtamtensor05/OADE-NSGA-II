"""Regression: Cairo font batches must not bridge disconnected text labels."""
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import patch

from research.plotting.qa.audit_figure_collisions import extract_pdf_geometry, audit_geometries


class BatchedFontTraceTests(unittest.TestCase):
    def audit(self, stroke_y):
        class Page:
            rect = (0, 0, 200, 120)

            def get_texttrace(self):
                return [{"bbox": (30, 20, 170, 90), "chars": [(ord(c),) for c in "FirstSecond"]}]

            def get_text(self, mode):
                return {"blocks": [{"type": 0, "lines": [
                    {"spans": [{"text": "First", "bbox": (30, 20, 60, 30)}]},
                    {"spans": [{"text": "Second", "bbox": (130, 80, 170, 90)}]},
                ]}]}

            def get_drawings(self):
                return [{"type": "s", "rect": (10, stroke_y, 190, stroke_y), "width": 1.0,
                         "items": [("l", SimpleNamespace(x=10, y=stroke_y), SimpleNamespace(x=190, y=stroke_y))]}]

            def get_images(self, full=True):
                return []

        class Document(list):
            def close(self):
                pass

        with patch.dict(sys.modules, {"pymupdf": SimpleNamespace(open=lambda _: Document([Page()]))}):
            return audit_geometries(extract_pdf_geometry(Path("unused.pdf")))

    def test_stroke_between_labels_is_not_a_collision(self):
        self.assertEqual(self.audit(60)["verdict"], "PASS")

    def test_stroke_through_actual_label_still_fails(self):
        result = self.audit(85)
        self.assertEqual(result["verdict"], "FIX BEFORE DELIVERY")
        self.assertTrue(any(row["kind"] == "text-stroke" for row in result["findings"]))
