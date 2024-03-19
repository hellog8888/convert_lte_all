import os


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def dms2dd(dd):
    N = dd[:2] + ' ' + dd[3:5] + ' ' + dd[5:7]
    E = dd[8:10] + ' ' + dd[11:13] + ' ' + dd[13:]
    d1, m1, s1 = N.split(' ')
    d2, m2, s2 = E.split(' ')
    try:
        return f'{toFixed((int(d2) + int(m2) / 60 + int(s2) / 3600), 6)} {toFixed((int(d1) + int(m1) / 60 + int(s1) / 3600), 6)}'
    except ValueError:
        pass


def convert_csv_to_txt():
    with open(f'lib/temp_folder/LTE_R&S LTE Scanner_[1]_trans_list_[].csv', mode="r", encoding='utf-8') as csv_file, \
            open(f'lib/temp_folder/LTE_R&S LTE Scanner_[1]_trans_list_[].txt', mode='w', encoding='utf-8') as txt_file:
        csv_file.seek(195)
        txt_file.write(csv_file.read())