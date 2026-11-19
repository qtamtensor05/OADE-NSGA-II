import unittest
import tempfile
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree
import numpy as np
from research.benchmarking.deb_metrics import convergence_metric, diversity_metric, zdt_reference
from research.benchmarking.deb_report import export_tables


class DebMetricsTests(unittest.TestCase):
    def test_convergence_direction_and_zero(self):
        ref=np.tile([[0.,1.],[1.,0.]],(250,1))
        self.assertEqual(convergence_metric([[0,1],[1,0]],ref),0.)
        self.assertAlmostEqual(convergence_metric([[0,2],[2,0]],ref),1.)

    def test_delta_hand_calculation_and_dominated_filter(self):
        self.assertEqual(diversity_metric([[0,1],[.5,.5],[1,0],[2,2]],[[0,1],[1,0]]),0.)
        self.assertAlmostEqual(diversity_metric([[0,1],[.25,.75],[1,0]],[[0,1],[1,0]]),.5)

    def test_degenerate(self):
        ref,_=zdt_reference('zdt1')
        self.assertIsNone(convergence_metric([],ref))
        for f in ([],[[0,1]],[[0,1],[0,1]]):
            self.assertIsNone(diversity_metric(f,[[0,1],[1,0]]))
        self.assertEqual(convergence_metric([[0,1]],ref),0.)

    def test_references_and_repeatability(self):
        for name in ('zdt1','zdt2','zdt3','zdt4','zdt6'):
            a,e=zdt_reference(name); b,_=zdt_reference(name)
            self.assertEqual(a.shape,(500,2)); np.testing.assert_array_equal(a,b)
            self.assertEqual(convergence_metric(a,a),0.)
            np.testing.assert_array_equal(e,a[[0,-1]])
        with self.assertRaises(ValueError): zdt_reference('dtlz1')

    def test_export_population_variance_and_xlsx(self):
        rows=[dict(algorithm='A',problem='zdt2',seed=i,valid=True,final_f=[[0,1+v],[1+v,0]],
                   n_eval=100,evaluation_budget=100,runtime_seconds=1) for i,v in enumerate((0.,2.))]
        with tempfile.TemporaryDirectory() as tmp:
            details=export_tables(rows,tmp,{'problems':[{'name':'zdt2'}],'global':{'pop_size':10}})
            vals=[r['upsilon'] for r in details]
            import csv
            with (Path(tmp)/'convergence_metric_results.csv').open() as handle:
                table=list(csv.reader(handle))
            self.assertAlmostEqual(float(table[1][1]),np.mean(vals))
            self.assertAlmostEqual(float(table[2][1]),np.var(vals,ddof=0))
            with ZipFile(Path(tmp)/'experimental_results.xlsx') as z:
                for name in z.namelist(): ElementTree.fromstring(z.read(name))


if __name__=='__main__': unittest.main()
