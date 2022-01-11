import os
import subprocess
import json
import sys

import utils.custom_log as docker_log


def read_100():
    list_100 = ['https://www.tsmc.com/', 'http://www.foxconn.com/', 'https://www.mediatek.com/',
                'http://www.fpcc.com.tw', 'https://www.cht.com.tw', 'https://www.fubon.com',
                'https://www.cathayholdings.com', 'http://www.umc.com/English/', 'https://www.deltaww.com/',
                'https://www.npc.com.tw', 'https://www.evergreen-marine.com/', 'http://www.fpcusa.com/',
                'http://www.csc.com.tw', 'http://www.aseglobal.com/en/', 'https://www.wanhai.com/',
                'http://www.fcfc.com.tw', 'http://www.ctbcholding.com', 'https://www.emega.com.tw/',
                'https://www.yangming.com/', 'https://www.uni-president.com.tw', 'https://www.silergy.com/',
                'http://www.chaileaseholding.com/', 'https://www.gw-semi.com/', 'http://www.largan.com.tw',
                'https://www.esunfhc.com/en', 'https://pressroom.hotaimotor.com.tw', 'https://www.yuanta.com',
                'https://www.quantatw.com', 'https://www.advantech.com/', 'http://ir.firstholding.com.tw',
                'http://www.tcfhc.com.tw', 'https://www.realtek.com/', 'http://www.fmt.com.tw/',
                'http://www.taiwancement.com/en/', 'http://www.novatek.com.tw/en-global/Home/Index',
                'https://english.taiwanmobile.com/', 'http://www.nanyapcb.com.tw/', 'http://www.hnfhc.com.tw',
                'http://www.vis.com.tw/', 'http://www.yageo.com', 'https://www.asus.com', 'https://www.powerchip.com/',
                'http://www.unimicron.com/', 'https://www.cdibh.com', 'http://www.nanya.com/en/',
                'https://www.taishinholdings.com.tw/', 'https://www.scsb.com.tw/', 'https://www.fetnet.net',
                'http://www.fengtay.com', 'http://www.innolux.com', 'http://www.bankchb.com/',
                'http://www.pegatroncorp.com/', 'https://www.thsrc.com.tw', 'https://www.wiwynn.com/',
                'https://www.auo.com/zh-TW', 'https://global.airtac.com/', 'http://www.fenc.com',
                'http://www.sinopac.com/en/index.html', 'https://www.asmedia.com.tw/', 'https://www.accton.com/',
                'https://www.acc.com.tw/', 'http://www.eclat.com.tw/zh-tw/', 'https://www.winfoundry.com/',
                'https://www.liteon.com/en-us', 'https://www.viseratech.com/', 'http://www.catcher.com.tw',
                'http://www.shinkonggroup.com/en/sk_financial.html', 'https://www.giant-bicycles.com/',
                'http://www.nienmade.com/', 'https://www.ememory.com.tw/', 'https://www.winbond.com/',
                'https://www.csttires.com', 'https://www.saswafer.com/', 'https://www.msi.com/',
                'https://www.hiwin.com/', 'https://voltronicpower.com/', 'http://www.ruentex.com.tw/',
                'https://www.sesa.it/', 'https://www.compal.com/', 'http://www.pouchen.com', 'https://www.evaair.com/',
                'http://www.china-airlines.com/', 'https://www.merida-bikes.com/en/', 'https://www.zdtco.com/',
                'https://www.walsin.com/', 'http://www.synnex-grp.com/en', 'http://www.kinsus.com.tw/',
                'https://www.eink.com/', 'https://www.inventec.com/', 'http://www.pti.com.tw/',
                'https://www.phison.com/', 'http://www.aspeedtech.com/', 'https://www.wpgholdings.com/',
                'http://www.tachen.com.tw/', 'https://www.emctw.com/en-global', 'https://www.wistron.com/',
                'https://www.acer.com/worldwide/', 'https://www.mxic.com.tw/', 'https://www.yulon-motor.com.tw/',
                'https://www.tatung.com/']

    temp_dict = {}

    for temp_url in list_100:
        print(temp_url)
        # temp_json = {'URL': temp_url, 'DATA': read_web(temp_url)}
        temp_dict[temp_url] = read_web(temp_url)

    with open('app.json', 'w') as f:
        json.dump(temp_dict, f)


def read_web(input_url):
    # 0.init
    result_list = []
    # 1. wappalyzer
    try:
        # 1.1 not in docker
        env = os.environ.get('ENV', 'test')
        if env == 'test':
            cmd = ['docker',
                   'run',
                   '--rm',
                   'test_1',
                   'node',
                   'src/drivers/npm/cli.js',
                   input_url]
        # 1.2 in docker
        else:
            cmd = ['node',
                   'src/drivers/npm/cli.js',
                   input_url]
        cmd_result = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=60)
        cmd_output = cmd_result.stdout.decode('utf-8')
        temp_list = cmd_output.split('\n')
        for str_output in temp_list:
            if 'urls' in str_output:
                cmd_output = str_output
        cmd_json = json.loads(cmd_output)
        for temp_technologies in cmd_json['technologies']:
            if temp_technologies['name']:
                if temp_technologies['version']:
                    result_list.append({"name": temp_technologies['name'], "version": temp_technologies['version']})
                    docker_log.info('name: ' + temp_technologies['name'])
                    docker_log.info('version: ' + temp_technologies['version'])
                else:
                    result_list.append({"name": temp_technologies['name'], "version": "0"})
                    docker_log.info('name: ' + temp_technologies['name'])
                    docker_log.info('version: 0')

    except Exception as ex:
        docker_log.error(ex)
    return result_list


if __name__ == '__main__':
    read_100()
    """
    try:
        unit_result_list = read_web("https://www.tainan.gov.tw/")
        for unit_result in unit_result_list:
            if 'Highcharts' in unit_result['name']:
                print('unit test(app_wapplyzer.py): pass')
                sys.exit(0)
    except Exception as unit_ex:
        print(unit_ex)
    print('unit test(app_wapplyzer.py): fail')
    """
    sys.exit(1)
