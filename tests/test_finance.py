import unittest
from pyspark.sql import SparkSession
from pyspark.sql import Row
from src.transformation import apply_financial_logic

# สร้าง SparkSession สำหรับทดสอบ
class TestFinancialMath(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .master("local[1]") \
            .appName("unit-tests") \
            .getOrCreate()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_uppercase_item_name(self):
        """
        ตรวจสอบว่า apply_financial_logic จะสร้างคอลัมน์
        `item_name_upper` โดยแปลงชื่อไอเทมเป็นตัวพิมพ์ใหญ่
        """
        # เตรียมข้อมูลตัวอย่าง
        data = [
            ("user1", "gold pass", "USD", 100.0),
            ("user2", "gem pack", "THB", 250.0),
        ]
        schema = ["user_id", "item_name", "currency", "amount_local"]
        df = self.spark.createDataFrame(data, schema)

        # เรียกฟังก์ชันที่ต้องการทดสอบ
        result = apply_financial_logic(df, None)

        # รวบรวมผลลัพธ์และตรวจสอบ
        collected = {row["user_id"]: row["item_name_upper"] for row in result.collect()}
        self.assertEqual(collected["user1"], "GOLD PASS")
        self.assertEqual(collected["user2"], "GEM PACK")

if __name__ == '__main__':
    unittest.main()