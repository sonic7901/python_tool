import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


def write_score(input_score):
    bk_img = cv2.imread("temp_score.jpg")
    font_path = "MSJH.ttf"
    font = ImageFont.truetype(font_path, 600)
    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)
    draw.text((650, 360), str(input_score), font=font, fill=(255, 255, 255))
    bk_img = np.array(img_pil)
    cv2.imwrite("temp_score.jpg", bk_img)


def write_score_100():
    bk_img = cv2.imread("temp_score.jpg")
    font_path = "MSJH.ttf"
    font = ImageFont.truetype(font_path, 530)
    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)
    draw.text((535, 400), "100", font=font, fill=(255, 255, 255))
    bk_img = np.array(img_pil)
    cv2.imwrite("temp_score.jpg", bk_img)


def write_result(input_list):
    bk_img = cv2.imread("grid.png")
    font_path = "MSJH.ttf"
    font = ImageFont.truetype(font_path, 20)
    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)
    count_hl = 0
    count_ml = 0
    count_ll = 0
    count_hm = 0
    count_mm = 0
    count_lm = 0
    count_hh = 0
    count_mh = 0
    count_lh = 0
    for temp_input in input_list:
        if len(temp_input['name']) > 20:
            temp_issue_name = '[' + str(temp_input['id']) + '] ' + temp_input['name'][:20] + '…'
        else:
            temp_issue_name = '[' + str(temp_input['id']) + '] ' + temp_input['name']
        if temp_input['level'] == '高' and temp_input['cost'] == 'Low':
            if count_hl > 6:
                continue
            elif count_hl == 6:
                draw.text((932, 110 + count_hl * 25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((932, 110 + count_hl * 25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_hl += 1
        if temp_input['level'] == '中' and temp_input['cost'] == 'Low':
            if count_ml > 6:
                continue
            elif count_ml == 6:
                draw.text((510, 110 + count_ml*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((510, 110 + count_ml*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_ml += 1
        if temp_input['level'] == '低' and temp_input['cost'] == 'Low':
            if count_ll > 6:
                continue
            elif count_ll == 6:
                draw.text((88, 110 + count_ll*25),
                          '⋮',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((88, 110 + count_ll*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_ll += 1
        if temp_input['level'] == '高' and temp_input['cost'] == 'Medium':
            if count_hm > 6:
                continue
            elif count_hm == 6:
                draw.text((932, 310 + count_hm*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((932, 310 + count_hm*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_hm += 1
        if temp_input['level'] == '中' and temp_input['cost'] == 'Medium':
            if count_mm > 6:
                continue
            elif count_mm == 6:
                draw.text((510, 310 + count_mm*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((510, 310 + count_mm*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_mm += 1
        if temp_input['level'] == '低' and temp_input['cost'] == 'Medium':
            if count_lm > 6:
                continue
            elif count_lm == 6:
                draw.text((88, 310 + count_lm*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((88, 310 + count_lm*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_lm += 1
        if temp_input['level'] == '高' and temp_input['cost'] == 'High':
            if count_hh > 6:
                continue
            elif count_hh == 6:
                draw.text((932, 510 + count_hh*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((932, 510 + count_hh*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_hh += 1
        if temp_input['level'] == '中' and temp_input['cost'] == 'High':
            if count_mh > 6:
                continue
            elif count_mh == 6:
                draw.text((510, 510 + count_mh*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((510, 510 + count_mh*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_mh += 1
        if temp_input['level'] == '低' and temp_input['cost'] == 'High':
            if count_lh > 6:
                continue
            elif count_lh == 6:
                draw.text((88, 510 + count_lh*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((88, 510 + count_lh*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_lh += 1
    bk_img = np.array(img_pil)
    cv2.imwrite("temp_grid.png", bk_img)


def write_result_en(input_list):
    bk_img = cv2.imread("grid.png")
    font_path = "MSJH.ttf"
    font = ImageFont.truetype(font_path, 20)
    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)
    count_hl = 0
    count_ml = 0
    count_ll = 0
    count_hm = 0
    count_mm = 0
    count_lm = 0
    count_hh = 0
    count_mh = 0
    count_lh = 0
    for temp_input in input_list:
        temp_issue_name = ''
        if len(temp_input['name']) > 20:
            temp_issue_name = '[' + str(temp_input['id']) + '] ' + temp_input['name'][:20] + '…'
        else:
            temp_issue_name = '[' + str(temp_input['id']) + '] ' + temp_input['name']
        if temp_input['level'] == 'High ' and temp_input['cost'] == 'Low':
            if count_hl > 6:
                continue
            elif count_hl == 6:
                draw.text((932, 110 + count_hl * 25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((932, 110 + count_hl * 25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_hl += 1
        if temp_input['level'] == 'Medium ' and temp_input['cost'] == 'Low':
            if count_ml > 6:
                continue
            elif count_ml == 6:
                draw.text((510, 110 + count_ml*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((510, 110 + count_ml*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_ml += 1
        if temp_input['level'] == 'Low ' and temp_input['cost'] == 'Low':
            if count_ll > 6:
                continue
            elif count_ll == 6:
                draw.text((88, 110 + count_ll*25),
                          '⋮',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((88, 110 + count_ll*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_ll += 1
        if temp_input['level'] == 'High ' and temp_input['cost'] == 'Medium':
            if count_hm > 6:
                continue
            elif count_hm == 6:
                draw.text((932, 310 + count_hm*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((932, 310 + count_hm*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_hm += 1
        if temp_input['level'] == 'Medium ' and temp_input['cost'] == 'Medium':
            if count_mm > 6:
                continue
            elif count_mm == 6:
                draw.text((510, 310 + count_mm*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((510, 310 + count_mm*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_mm += 1
        if temp_input['level'] == 'Low' and temp_input['cost'] == 'Medium':
            if count_lm > 6:
                continue
            elif count_lm == 6:
                draw.text((88, 310 + count_lm*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((88, 310 + count_lm*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_lm += 1
        if temp_input['level'] == 'High ' and temp_input['cost'] == 'High':
            if count_hh > 6:
                continue
            elif count_hh == 6:
                draw.text((932, 510 + count_hh*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((932, 510 + count_hh*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_hh += 1
        if temp_input['level'] == 'Medium ' and temp_input['cost'] == 'High':
            if count_mh > 6:
                continue
            elif count_mh == 6:
                draw.text((510, 510 + count_mh*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((510, 510 + count_mh*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_mh += 1
        if temp_input['level'] == 'Low ' and temp_input['cost'] == 'High':
            if count_lh > 6:
                continue
            elif count_lh == 6:
                draw.text((88, 510 + count_lh*25),
                          '…',
                          font=font,
                          fill=(0, 0, 0))
            else:
                draw.text((88, 510 + count_lh*25),
                          temp_issue_name,
                          font=font,
                          fill=(0, 0, 0))
            count_lh += 1
    bk_img = np.array(img_pil)
    cv2.imwrite("temp_grid.png", bk_img)


if __name__ == '__main__':
    main_list = [{'name': '中文測試', 'id': 'VAS01', 'level': '高', 'cost': 'Low'},
                 {'name': 'test name', 'id': 'VAS02', 'level': '中', 'cost': 'Low'},
                 {'name': 'test name', 'id': 'VAS03', 'level': '低', 'cost': 'Low'},
                 {'name': 'test name', 'id': 'VAS04', 'level': '高', 'cost': 'Medium'},
                 {'name': 'test name', 'id': 'VAS05', 'level': '中', 'cost': 'Medium'},
                 {'name': 'test name', 'id': 'VAS06', 'level': '低', 'cost': 'Medium'},
                 {'name': 'test name', 'id': 'VAS07', 'level': '高', 'cost': 'High'},
                 {'name': 'test name', 'id': 'VAS08', 'level': '中', 'cost': 'High'},
                 {'name': 'test name', 'id': 'VAS09', 'level': '低', 'cost': 'High'},
                 {'name': 'test name', 'id': 'VAS11', 'level': '高', 'cost': 'Low'},
                 {'name': 'test name', 'id': 'VAS12', 'level': '中', 'cost': 'Low'},
                 {'name': 'test name', 'id': 'VAS13', 'level': '低', 'cost': 'Low'},
                 {'name': 'test name', 'id': 'VAS14', 'level': '高', 'cost': 'Medium'},
                 {'name': 'test name', 'id': 'VAS15', 'level': '中', 'cost': 'Medium'},
                 {'name': 'test name', 'id': 'VAS16', 'level': '低', 'cost': 'Medium'},
                 {'name': 'test name', 'id': 'VAS17', 'level': '高', 'cost': 'High'},
                 {'name': 'test name', 'id': 'VAS18', 'level': '中', 'cost': 'High'},
                 {'name': 'test name', 'id': 'VAS19', 'level': '低', 'cost': 'High'},
                 {'name': 'test name', 'id': 'VAS21', 'level': '高', 'cost': 'Low'},
                 {'name': 'test name', 'id': 'VAS31', 'level': '高', 'cost': 'Low'},
                 {'name': 'test name', 'id': 'VAS41', 'level': '高', 'cost': 'Low'},
                 {'name': 'test name', 'id': 'VAS51', 'level': '高', 'cost': 'Low'},
                 {'name': 'test name', 'id': 'VAS61', 'level': '高', 'cost': 'Low'}]
    write_result(main_list)
    write_score_100()
    # write_text(95)
    # zap_score(3, 2, 9)
    # zap_pie(3, 2, 9)
