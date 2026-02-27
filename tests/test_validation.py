import unittest
from pyspark.sql import SparkSession
from pyspark.sql import Row
from src.validation import check_data_integrity

class TestValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder.master("local[1]").appName("validation-tests").getOrCreate()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_data_integrity_matches(self):
        # both sides sum to same amount
        data1 = [("a", 10.0), ("b", 5.0)]
        data2 = [("x", 7.5), ("y", 7.5)]
        df1 = self.spark.createDataFrame(data1, ["id", "amount_usd"])
        df2 = self.spark.createDataFrame(data2, ["id", "amount_usd"])
        self.assertTrue(check_data_integrity(df1, df2))

    def test_data_integrity_differs(self):
        data1 = [("a", 10.0)]
        data2 = [("x", 5.0)]
        df1 = self.spark.createDataFrame(data1, ["id", "amount_usd"])
        df2 = self.spark.createDataFrame(data2, ["id", "amount_usd"])
        self.assertFalse(check_data_integrity(df1, df2))

    def test_data_integrity_with_tiny_difference(self):
        # difference just under tolerance threshold should still be True
        data1 = [("a", 10.005)]
        data2 = [("x", 10.0)]
        df1 = self.spark.createDataFrame(data1, ["id", "amount_usd"])
        df2 = self.spark.createDataFrame(data2, ["id", "amount_usd"])
        self.assertTrue(check_data_integrity(df1, df2))

    def test_data_integrity_empty_frames(self):
        # when both are empty sums will be None, should handle gracefully
        from pyspark.sql.types import StructType, StructField, StringType, DoubleType

        schema = StructType([
            StructField("id", StringType(), True),
            StructField("amount_usd", DoubleType(), True),
        ])
        df1 = self.spark.createDataFrame(self.spark.sparkContext.emptyRDD(), schema)
        df2 = self.spark.createDataFrame(self.spark.sparkContext.emptyRDD(), schema)
        # calling should not raise and should return True (0 vs 0)
        self.assertTrue(check_data_integrity(df1, df2))

if __name__ == '__main__':
    unittest.main()
