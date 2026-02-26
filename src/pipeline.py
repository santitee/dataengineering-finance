import sys
import os
from pyspark.sql import SparkSession

# ดัน Root Folder เข้าไปในระบบของ Python
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.transformation import apply_financial_logic, get_top_spenders

def run_pipeline(mode):
    spark = SparkSession.builder.appName(f"Supercell_Finance_{mode}").getOrCreate()
    
    print(f"\n--- Processing Mode: {mode.upper()} ---")

    # กำหนด Path ไปยังไฟล์ Mockup Data
    mock_data_path = os.path.join(project_root, 'data', 'samples', 'financial_mockup_data.csv')
    
    # ตรวจสอบว่ามีไฟล์หรือไม่ ถ้าไม่มีให้หยุดทำงาน
    if not os.path.exists(mock_data_path):
        print(f"❌ Error: ไม่พบไฟล์ข้อมูลที่ {mock_data_path}")
        print("💡 กรุณารัน 'python src/mockup_data.py' ก่อนครับ")
        sys.exit(1)

    # อ่านข้อมูลด้วย PySpark
    print("📥 Loading Data...")
    df_raw = spark.read.csv(mock_data_path, header=True, inferSchema=True)
    
    # จำลอง DataFrame สำหรับ FX Rates (อัตราแลกเปลี่ยน)
    df_fx = spark.createDataFrame([("USD", 1.0)], ["currency", "rate"])

    if mode == "nrt":
        print("⚡ Running Near Real-Time (30 min window)...")
    elif mode == "daily":
        print("📅 Running Daily Batch (Signal Triggered)...")
    elif mode == "monthly":
        print("🏦 Running Monthly Closing (Financial Audit)...")

    # เรียกใช้ Logic จาก transformation.py
    processed_df = apply_financial_logic(df_raw, df_fx)
    top_users = get_top_spenders(processed_df)
    
    # แสดงผล
    print("\n🌟 Top 10 Spenders:")
    top_users.show()

if __name__ == "__main__":
    mode_arg = sys.argv[1] if len(sys.argv) > 1 else "nrt"
    run_pipeline(mode_arg)