import custom_report

if __name__ == '__main__':
    # example start
    custom_report.set_company('鉅祥企業股份有限公司')
    custom_report.set_date_start('2023/1/31')
    custom_report.set_date_end('2023/2/2')
    custom_report.transfer_report()
