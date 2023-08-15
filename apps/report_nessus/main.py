import custom_report

if __name__ == '__main__':
    # example start
    custom_report.set_company('臺灣水泥股份有限公司')
    custom_report.set_date_start('2023/8/8')
    custom_report.set_date_end('2023/8/9')
    custom_report.transfer_report()
