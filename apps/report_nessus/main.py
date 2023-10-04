import custom_report

if __name__ == '__main__':
    # example start
    custom_report.set_company('example')
    custom_report.set_date_start('2023/1/1')
    custom_report.set_date_end('2023/1/2')
    custom_report.transfer_report()
