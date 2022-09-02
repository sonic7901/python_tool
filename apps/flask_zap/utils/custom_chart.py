import pathlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import utils.custom_image

# file path
template_path = str(pathlib.Path(__file__).parent.absolute()) + "\\"


def zap_pie(input_low, input_medium, input_high):
    try:
        labels = '低 : ' + str(input_low), '中 : ' + str(input_medium), '高 : ' + str(input_high)
        sizes = [input_low, input_medium, input_high]
        plt_pie(template_path + "temp_distribution.jpg", labels, sizes)
    except Exception as ex:
        print(ex)


def zap_pie_en(input_low, input_medium, input_high):
    try:
        labels = 'Low : ' + str(input_low), 'Medium : ' + str(input_medium), 'High : ' + str(input_high)
        sizes = [input_low, input_medium, input_high]
        plt_pie(template_path + "temp_distribution.jpg", labels, sizes)
    except Exception as ex:
        print(ex)


def zap_score(input_low, input_medium, input_high):
    try:
        temp_score = 100 - int(input_low) - int(input_medium)*2 - int(input_high)*3
        if temp_score < 60:
            temp_score = 60
        plt_score(temp_score, template_path + 'temp_score.jpg')
    except Exception as ex:
        print(ex)


def plt_pie(input_filename, input_labels, input_values):
    try:
        temp_colors = ['#72B347', '#F5C000', '#F37925']
        patches, l_text, p_text = plt.pie(input_values,
                                          labels=input_labels,
                                          colors=temp_colors,
                                          autopct='',
                                          startangle=90)
        # force change font for chinese
        temp_font = fm.FontProperties(fname=template_path + "MSJH.ttf")
        temp_font.set_weight('bold')
        for p in l_text:
            p.set_fontproperties(temp_font)

        plt.pie([1, 0, 0], radius=0.7, colors='w')
        plt.axis('equal')
        plt.savefig(input_filename, dpi=400, bbox_inches='tight', pad_inches=0)
        plt.close()
    except Exception as ex:
        print(ex)


def plt_score(input_score, input_filename):
    try:
        if input_score > 80:
            input_values = [1, 0, 0]
            out_colors = '#72B347'
            in_colors = '#61A237'
        elif 80 > input_score > 60:
            input_values = [0, 1, 0]
            out_colors = '#F5C000'
            in_colors = '#E4B000'
        elif input_score < 60:
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
            utils.custom_image.write_score_100()
        else:
            utils.custom_image.write_score(input_score)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    zap_score(3, 2, 9)
    zap_pie(3, 2, 9)


