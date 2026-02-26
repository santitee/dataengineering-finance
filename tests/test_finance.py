import unittest
from transformation import apply_financial_logic
# สร้าง Mock Spark Session สำหรับ Test

class TestFinancialMath(unittest.TestCase):
    def test_net_revenue_calculation(self):
        # ทดสอบว่าถ้าซื้อ 100 USD รายได้สุทธิต้องเป็น 70 USD (หลังหัก 30%)
        # จัดทำ Mock DataFrame และ Assert ผลลัพธ์ที่นี่
        pass

if __name__ == '__main__':
    unittest.main()