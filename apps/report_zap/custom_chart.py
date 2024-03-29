import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import custom_image


def zap_pie(input_low, input_medium, input_high):
    try:
        if input_low == 0:
            if input_medium == 0:
                labels = ['高 : ' + str(input_high)]
                sizes = [input_high]
                temp_colors = ['#F37925']
            elif input_high == 0:
                labels = ['中 : ' + str(input_medium)]
                sizes = [input_medium]
                temp_colors = ['#F5C000']
            else:
                labels = ['中 : ' + str(input_medium), '高 : ' + str(input_high)]
                sizes = [input_medium, input_high]
                temp_colors = ['#F5C000', '#F37925']
        elif input_medium == 0:
            if input_low == 0:
                labels = ['高 : ' + str(input_high)]
                sizes = [input_high]
                temp_colors = ['#F37925']
            elif input_high == 0:
                labels = ['低 : ' + str(input_low)]
                sizes = [input_low]
                temp_colors = ['#72B347']
            else:
                labels = ['低 : ' + str(input_low), '高 : ' + str(input_high)]
                sizes = [input_low, input_high]
                temp_colors = ['#72B347', '#F37925']
        elif input_high == 0:
            if input_low == 0:
                labels = ['中 : ' + str(input_medium)]
                sizes = [input_medium]
                temp_colors = ['#F5C000']
            elif input_medium == 0:
                labels = ['低 : ' + str(input_low)]
                sizes = [input_low]
                temp_colors = ['#72B347']
            else:
                labels = ['低 : ' + str(input_low), '中 : ' + str(input_medium)]
                sizes = [input_low, input_medium]
                temp_colors = ['#72B347', '#F5C000']
        else:
            labels = ['低 : ' + str(input_low), '中 : ' + str(input_medium), '高 : ' + str(input_high)]
            sizes = [input_low, input_medium, input_high]
            temp_colors = ['#72B347', '#F5C000', '#F37925']

        patches, l_text, p_text = plt.pie(sizes,
                                          labels=list(labels),
                                          colors=temp_colors,
                                          autopct='',
                                          startangle=90)
        # force change font for chinese
        temp_font = fm.FontProperties(fname="MSJH.ttf")
        temp_font.set_weight('bold')
        for p in l_text:
            p.set_fontproperties(temp_font)

        plt.pie([1, 0, 0], radius=0.7, colors='w')
        plt.axis('equal')
        plt.savefig("temp_distribution.jpg", dpi=400, bbox_inches='tight', pad_inches=0)
        plt.close()
    except Exception as ex:
        print(ex)


def zap_pie_en(input_low, input_medium, input_high):
    try:
        if input_low == 0:
            if input_medium == 0:
                labels = ['High : ' + str(input_high)]
                sizes = [input_high]
                temp_colors = ['#F37925']
            elif input_high == 0:
                labels = ['Medium : ' + str(input_medium)]
                sizes = [input_medium]
                temp_colors = ['#F5C000']
            else:
                labels = ['Medium : ' + str(input_medium), 'High : ' + str(input_high)]
                sizes = [input_medium, input_high]
                temp_colors = ['#F5C000', '#F37925']
        elif input_medium == 0:
            if input_low == 0:
                labels = ['High : ' + str(input_high)]
                sizes = [input_high]
                temp_colors = ['#F37925']
            elif input_high == 0:
                labels = ['Low : ' + str(input_low)]
                sizes = [input_low]
                temp_colors = ['#72B347']
            else:
                labels = ['Low : ' + str(input_low), 'High : ' + str(input_high)]
                sizes = [input_low, input_high]
                temp_colors = ['#72B347', '#F37925']
        elif input_high == 0:
            if input_low == 0:
                labels = ['Medium : ' + str(input_medium)]
                sizes = [input_medium]
                temp_colors = ['#F5C000']
            elif input_medium == 0:
                labels = ['Low : ' + str(input_low)]
                sizes = [input_low]
                temp_colors = ['#72B347']
            else:
                labels = ['Low : ' + str(input_low), 'Medium : ' + str(input_medium)]
                sizes = [input_low, input_medium]
                temp_colors = ['#72B347', '#F5C000']
        else:
            labels = ['Low : ' + str(input_low), 'Medium : ' + str(input_medium), 'High : ' + str(input_high)]
            sizes = [input_low, input_medium, input_high]
            temp_colors = ['#72B347', '#F5C000', '#F37925']

        patches, l_text, p_text = plt.pie(sizes,
                                          labels=list(labels),
                                          colors=temp_colors,
                                          autopct='',
                                          startangle=90)
        # force change font for chinese
        temp_font = fm.FontProperties(fname="MSJH.ttf")
        temp_font.set_weight('bold')
        for p in l_text:
            p.set_fontproperties(temp_font)

        plt.pie([1, 0, 0], radius=0.7, colors='w')
        plt.axis('equal')
        plt.savefig("temp_distribution.jpg", dpi=400, bbox_inches='tight', pad_inches=0)
        plt.close()
    except Exception as ex:
        print(ex)


def zap_score(input_low, input_medium, input_high, input_count):
    try:
        temp_dis = int(input_count)
        if temp_dis == 0:
            temp_score = 100
        else:
            temp_score = 100 - int(input_low/temp_dis) - int(input_medium*2/temp_dis) - int(input_high*3/temp_dis)
            if temp_score < 60:
                temp_score = 60
        plt_score(temp_score, 'temp_score.jpg')
    except Exception as ex:
        print(ex)


def plt_score(input_score, input_filename):
    try:
        input_values = [0, 0, 0]
        out_colors = ""
        in_colors = ""
        if input_score >= 80:
            input_values = [1, 0, 0]
            out_colors = '#72B347'
            in_colors = '#61A237'
        elif 80 > input_score > 60:
            input_values = [0, 1, 0]
            out_colors = '#F5C000'
            in_colors = '#E4B000'
        elif input_score <= 60:
            input_values = [0, 0, 1]
            out_colors = '#F37925'
            in_colors = '#E26814'
        temp_colors = ['#72B347', '#F5C000', '#F37925']
        plt.pie(input_values,
                labels=[' ', ' ', ' '],
                colors=temp_colors,
                autopct='',
                startangle=90)
        plt.pie([1], radius=0.8, colors=[in_colors])
        plt.pie([1], radius=0.76, colors=[out_colors])
        plt.axis('equal')
        plt.savefig(input_filename, dpi=400, bbox_inches='tight', pad_inches=0.01)
        plt.close()
        if input_score == 100:
            custom_image.write_score_100()
        else:
            custom_image.write_score(input_score)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    zap_score(3, 3, 0, 2)
    zap_pie(3, 3, 0)


