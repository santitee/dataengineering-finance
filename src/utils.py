import logging
import json
import yaml
import os
from datetime import datetime

# ตั้งค่า Logging สำหรับติดตามการรัน Pipeline
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SupercellFinanceUtils")

def load_config(config_path):
    """โหลดไฟล์การตั้งค่า (YAML หรือ JSON)"""
    with open(config_path, 'r') as f:
        if config_path.endswith('.yaml') or config_path.endswith('.yml'):
            return yaml.safe_load(f)
        return json.load(f)

def check_upstream_signal(signal_name, date_str):
    """
    จำลองระบบ Signal-based Trigger
    เช็คว่า Upstream (เช่น Store Data หรือ FX Rate) พร้อมใช้งานสำหรับวันที่ระบุหรือไม่
    """
    # ในหน้างานจริง ส่วนนี้อาจจะเช็คการมีอยู่ของไฟล์ใน S3 หรือเช็คจาก Airflow Variable
    logger.info(f"Checking for signal: {signal_name} for date: {date_str}")
    
    # สมมติว่าคืนค่า True เสมอเพื่อการ Demo
    # แต่ในการสัมภาษณ์ให้บอกว่า "เราใช้ส่วนนี้เพื่อทำ Data Availability Check"
    return True

def log_process_metadata(mode, status, records_processed=0):
    """บันทึก Metadata การประมวลผลลงใน Log หรือ Database สำหรับ Audit Trail"""
    metadata = {
        "execution_time": datetime.now().isoformat(),
        "mode": mode,
        "status": status,
        "records_count": records_processed
    }
    logger.info(f"Process Metadata: {metadata}")
    return metadata

def get_fiscal_period(date_obj):
    """คืนค่าปีและเดือนเพื่อใช้ในการทำ Monthly Closing"""
    return date_obj.strftime("%Y-%m")