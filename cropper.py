import sys, os, re
from PIL import Image

desc =  "1行目に画像ファイルがあるディレクトリ、\n" \
        "2行目に画像ファイル名（拡張子含）を表す正規表現、\n" \
        "3行目以降に画像を切り出す座標を書いてください。\n" \
        "座標は矩形1つ毎に左上x座標, 左上y座標, 右下x座標, 右下y座標を半角カンマ区切りで入れてください。\n" \
        "ファイルの入出力は全てJPEGを前提にしています。"

args = sys.argv

if len(args) == 1 or args[1] in {'-h', 'help'}:
    print(desc)
else :
    with open(args[1], 'r') as f:
        #ディレクトリ名
        dirc = f.readline().rstrip()
        os.chdir(dirc)
        #ファイル名
        ptrn = re.compile(f.readline().rstrip())
        #ファイル名の一覧
        pic_names = [name for name in os.listdir(dirc) if ptrn.match(name)]
        #矩形の座標
        def convert_pos(text) :
            return tuple(int(x) for x in text.split(','))
        areas = [convert_pos(line) for line in f]

        for pname in pic_names :
            img = Image.open(pname, 'r')
            for i, area in enumerate(areas) :
                dir_name = str(i)
                if not os.path.exists(dir_name) :
                    os.mkdir(dir_name)
                new_img = img.crop(area)
                new_img.save(dir_name + '/' + pname, 'JPEG', quality=100, optimize=True)
