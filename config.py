from environs import Env
import os


env = Env()
env.read_env()

phone_number = env.str("phone_number")
wb_url = env.str("url")
url_report_3 = env.str("url_report_sales")
url_report_4 = env.str("url_report_brand_share")
url_report_11 = env.str("url_report_warehouse_remains")
dir_for_save_reports = env.str("dir_for_save_reports")