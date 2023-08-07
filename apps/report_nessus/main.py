import custom_report

if __name__ == '__main__':
    # example start
    custom_report.set_company('新應材股份有限公司')
    custom_report.set_date_start('2023/7/16')
    custom_report.set_date_end('2023/7/31')
    custom_report.transfer_report_en()
