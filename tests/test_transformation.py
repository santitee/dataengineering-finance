import unittest
from pyspark.sql import SparkSession
from pyspark.sql import Row
from src.transformation import apply_financial_logic, get_top_spenders

class TestTransformation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder.master("local[1]").appName("transformation-tests").getOrCreate()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_apply_financial_logic_adds_upper_column(self):
        data = [("u1", "itemA"), ("u2", "itemB")]
        df = self.spark.createDataFrame(data, ["user_id", "item_name"])
        out = apply_financial_logic(df, None)
        collected = {r.user_id: r.item_name_upper for r in out.collect()}
        self.assertEqual(collected["u1"], "ITEMA")
        self.assertEqual(collected["u2"], "ITEMB")

    def test_get_top_spenders_returns_sorted_results(self):
        data = [("a", 10.0), ("b", 30.0), ("a", 5.0)]
        df = self.spark.createDataFrame(data, ["supercell_id", "amount_usd"])
        top = get_top_spenders(df).collect()
        # expect two rows: b=30, a=15
        self.assertEqual(top[0]["supercell_id"], "b")
        self.assertAlmostEqual(top[0]["total_spent_usd"], 30.0)
        self.assertEqual(top[1]["supercell_id"], "a")
        self.assertAlmostEqual(top[1]["total_spent_usd"], 15.0)

    def test_get_top_spenders_handles_missing_column(self):
        # when amount_usd column is absent, original df should be returned
        data = [("x", "foo")]
        df = self.spark.createDataFrame(data, ["supercell_id", "currency"])
        out = get_top_spenders(df)
        self.assertEqual(out.collect(), df.collect())

    def test_apply_financial_logic_with_empty_dataframe(self):
        # ensure function can accept an empty DF and still add column
        from pyspark.sql.types import StructType, StructField, StringType

        schema = StructType([
            StructField("user_id", StringType(), True),
            StructField("item_name", StringType(), True),
        ])
        empty = self.spark.createDataFrame(self.spark.sparkContext.emptyRDD(), schema)
        out = apply_financial_logic(empty, None)
        self.assertIn("item_name_upper", out.columns)
        self.assertEqual(out.count(), 0)

if __name__ == '__main__':
    unittest.main()
