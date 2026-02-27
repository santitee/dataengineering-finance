from pyspark.sql import functions as F

def check_data_integrity(internal_df, store_report_df):
    """
    Reconciliation: ตรวจสอบว่ายอดในระบบเรา (Internal) 
    ตรงกับที่ Apple/Google รายงานมา (External) หรือไม่
    """
    internal_sum = internal_df.agg(F.sum("amount_usd")).collect()[0][0]
    store_sum = store_report_df.agg(F.sum("amount_usd")).collect()[0][0]
    # จัดการกรณี DataFrame ว่าง (sum คืนค่า None)
    internal_sum = internal_sum or 0.0
    store_sum = store_sum or 0.0
    
    diff = abs(internal_sum - store_sum)
    if diff > 0.01: # อนุโลมให้ผลต่างทศนิยมเล็กน้อย
        print(f"⚠️ Reconciliation Alert: Difference of ${diff}")
        return False
    
    print("✅ Data In-Sync")
    return True