# from pyspark.sql import functions as F

# def apply_financial_logic(df, fx_rates_df):
#     """
#     ประมวลผลข้อมูลการเงิน: แปลงค่าเงิน, คำนวณรายได้สุทธิ และสถานะการรับรู้รายได้
#     """
#     # Join ข้อมูลธุรกรรมกับอัตราแลกเปลี่ยน
#     df_joined = df.join(fx_rates_df, on="currency", how="left")
    
#     # 1. แปลงเป็น USD และหักค่าธรรมเนียม Store (30%)
#     df_transformed = df_joined.withColumn(
#         "amount_usd", F.round(F.col("amount_local") * F.col("rate_to_usd"), 2)
#     ).withColumn(
#         "platform_fee", F.round(F.col("amount_usd") * 0.30, 2)
#     ).withColumn(
#         "net_revenue", F.round(F.col("amount_usd") - F.col("platform_fee"), 2)
#     )
    
#     # 2. Revenue Recognition Logic (แยกรายได้รับรู้ทันที vs รอตัดบัญชี)
#     df_transformed = df_transformed.withColumn(
#         "revenue_status", 
#         F.when(F.col("item_name").isin("Gold Pass", "Gem Pack"), "DEFERRED")
#          .otherwise("RECOGNIZED")
#     )
    
#     return df_transformed

# def get_top_spenders(df, limit=10):
#     """คำนวณผู้เล่นที่มียอดใช้จ่ายสูงสุด (Whales Analysis)"""
#     return df.groupby("user_id") \
#              .agg(F.sum("amount_usd").alias("total_spent_usd")) \
#              .orderBy(F.desc("total_spent_usd")) \
#              .limit(limit)


from pyspark.sql import DataFrame
import pyspark.sql.functions as F

def apply_financial_logic(df_raw: DataFrame, df_fx: DataFrame) -> DataFrame:
    """
    จำลองการทำ Data Transformation ด้วย PySpark
    """
    print("⏳ Applying financial logic...")
    # ตัวอย่าง: แปลงชื่อไอเทมเป็นตัวพิมพ์ใหญ่
    df_transformed = df_raw.withColumn("item_name_upper", F.upper(F.col("item_name")))
    return df_transformed

def get_top_spenders(df: DataFrame) -> DataFrame:
    """
    หาผู้เล่นที่ใช้จ่ายสูงสุด (จำลอง)
    """
    print("🏆 Calculating top spenders...")
    # จัดกลุ่มตาม supercell_id และหายอดรวม amount_usd
    if "amount_usd" in df.columns:
        top_users = df.groupBy("supercell_id") \
                      .agg(F.sum("amount_usd").alias("total_spent_usd")) \
                      .orderBy(F.desc("total_spent_usd")) \
                      .limit(10)
        return top_users
    else:
        print("⚠️ Column 'amount_usd' not found, returning original DataFrame")
        return df