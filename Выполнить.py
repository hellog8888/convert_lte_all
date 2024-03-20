import os
import glob
import pandas as pd
from transliterate import translit
from lib.create_atd_file import create_atd_file
from lib.convert_functions import dms2dd, convert_csv_to_txt
from lib.add_functions import count_for_uniq, get_source_name, check_or_create_temp_folder, create_folder_and_move_files, check_or_create_source_folder


dict_for_operator = \
    {
        7740000076: '1',
        7812014560: '2',
        7701725181: '2',
        7707049388: '20',
        7743895280: '20',
        7713076301: '99',
    }


def main_stage(file_LTE_all):

    LTE_db = file_LTE_all.loc[:, ['Свидетельство', 'ИНН', 'Широта/ Долгота', 'Идентификационный номер РЭС в сети связи', 'Место установки']]

    for i in range(len(LTE_db['ИНН'])):
        if LTE_db['ИНН'][i] in dict_for_operator:
            LTE_db['ИНН'][i] = dict_for_operator[LTE_db['ИНН'][i]]

    LTE_db['Широта/ Долгота'] = [dms2dd(str(x)) for x in LTE_db['Широта/ Долгота']]
    LTE_db['PosLatitude'] = LTE_db['Широта/ Долгота'].str[:9]
    LTE_db['PosLongitude'] = LTE_db['Широта/ Долгота'].str[10:]
    LTE_db = LTE_db.drop(['Широта/ Долгота'], axis=1)

    LTE_db['Идентификационный номер РЭС в сети связи'] = \
        [str(x).replace('MCC, MNC, eNB ID, Cell ID: ', '').replace('CI(ECI): ', '').replace('CI (ECI): ', '').replace('MAC:', '').replace(';', ',')
         for x in LTE_db['Идентификационный номер РЭС в сети связи']]
    LTE_db['Идентификационный номер РЭС в сети связи'] = LTE_db['Идентификационный номер РЭС в сети связи'].str.replace(' ', '')

    LTE_db['Свидетельство'] = LTE_db['Свидетельство'].str.replace('  № ', '-')
    LTE_db['Свидетельство'] = LTE_db['Свидетельство'].str.replace(' ', '-')
    LTE_db['Место установки'] = LTE_db['Место установки'].str.replace('  ', '')
    LTE_db['Место установки'] = LTE_db['Место установки'].str.replace('.,', ',', regex=False)
    LTE_db['Место установки'] = LTE_db['Место установки'].str.replace('\"\"', '')
    LTE_db['Место установки'] = LTE_db['Место установки'].str.replace('\"', '')
    LTE_db['Место установки'] = LTE_db['Место установки'].str.replace('Краснодарский край, ', '')
    LTE_db['Место установки'] = LTE_db['Место установки'].str.replace('Адыгея Респ, ', '')
    LTE_db['Место установки'] = LTE_db['Место установки'].str.replace('Республика Адыгея (Адыгея), ', '', regex=False)
    LTE_db['Место установки'] = [str(translit(x, 'ru', reversed=True)) for x in LTE_db['Место установки']]
    LTE_db['eNodeB_Name'] = LTE_db['Свидетельство'] + '--' + LTE_db['Место установки']
    LTE_db = LTE_db.drop(['Свидетельство'], axis=1)
    LTE_db = LTE_db.drop(['Место установки'], axis=1)

    LTE_db['Идентификационный номер РЭС в сети связи'] = LTE_db['Идентификационный номер РЭС в сети связи'].str.split(',')
    LTE_db = LTE_db.explode('Идентификационный номер РЭС в сети связи')

    LTE_db = LTE_db[['eNodeB_Name', 'PosLongitude', 'PosLatitude', 'ИНН', 'Идентификационный номер РЭС в сети связи']]
    LTE_db.rename(columns={'ИНН': 'MNC', 'Идентификационный номер РЭС в сети связи': 'CellID'}, inplace=True)
    LTE_db['UniqueID'] = '0'
    LTE_db['UniqueID'] = [count_for_uniq() for _ in LTE_db['UniqueID']]
    LTE_db['MCC'] = '250'
    LTE_db['PosAltitude'] = '0.00'
    LTE_db['Power'] = '0.0000'
    LTE_db['PosErrorLargeHalfAxis'] = '0.00'
    LTE_db['PosErrorSmallHalfAxis'] = '0.00'
    LTE_db['PosErrorDirection'] = '0.00'
    LTE_db['Direction'] = '0.00'
    LTE_db['IsDirected'] = '1'
    LTE_db['3GNC'] = ''
    LTE_db['2GNC'] = ''
    LTE_db['4GNC'] = ''
    LTE_db['EARFCN'] = '0'
    LTE_db['PhyCellID'] = '0'
    LTE_db = LTE_db[['UniqueID', 'eNodeB_Name', 'MNC', 'MCC', 'PosLatitude', 'PosLongitude', 'PosAltitude', 'Power', 'PosErrorLargeHalfAxis', 'PosErrorSmallHalfAxis', 'PosErrorDirection', 'Direction', 'IsDirected', '3GNC', '2GNC', '4GNC', 'EARFCN', 'CellID', 'PhyCellID']]

    LTE_db.to_csv('./lib/temp_folder/LTE_R&S LTE Scanner_[1]_trans_list_[].csv', sep=';', index=False)


if __name__ == '__main__':

    print('1. Считывание файла')
    check_or_create_source_folder(f'lib\\temp_folder')
    source_file_name = str.strip(get_source_name('Исходный_файл'), '.xls')
    file_LTE_all = pd.read_excel(glob.glob('Исходный_файл/*.xls')[0])

    print('2. Выполнение...')
    check_or_create_temp_folder(f'lib\\temp_folder')
    main_stage(file_LTE_all)

    print('3. Создание результата')
    convert_csv_to_txt()
    os.remove(f'lib/temp_folder/LTE_R&S LTE Scanner_[1]_trans_list_[].csv')
    create_atd_file()
    create_folder_and_move_files(source_file_name)

    print('')
    print('Выполнено')
