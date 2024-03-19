def create_atd_file():
    with open('lib/temp_folder/LTE_R&S LTE Scanner_[1]_trans_list_[].atd', mode="w", encoding='utf-8') as adt_file:
        header_rows_db = """[Main]
Type=ATD
[Table1]
Name=LTE_PNS_DATABASE
File=LTE_R&S LTE Scanner_[1]_trans_list_[].txt
Columns_Size=19
Columns0_Name=UniqueID
Columns0_Type=utULInt
Columns1_Name=eNodeB_Name
Columns1_Type=utDynChar
Columns2_Name=MNC
Columns2_Type=utULInt
Columns3_Name=MCC
Columns3_Type=utULInt
Columns4_Name=PosLongitude
Columns4_Type=utDouble
Columns5_Name=PosLatitude
Columns5_Type=utDouble
Columns6_Name=PosAltitude
Columns6_Type=utDouble
Columns7_Name=Power
Columns7_Type=utDouble
Columns8_Name=PosErrorLargeHalfAxis
Columns8_Type=utDouble
Columns9_Name=PosErrorSmallHalfAxis
Columns9_Type=utDouble
Columns10_Name=PosErrorDirection
Columns10_Type=utDouble
Columns11_Name=Direction
Columns11_Type=utUSInt
Columns12_Name=IsDirected
Columns12_Type=utUTInt
Columns13_Name=3GNC
Columns13_Type=utDynChar
Columns14_Name=2GNC
Columns14_Type=utDynChar
Columns15_Name=4GNC
Columns15_Type=utDynChar
Columns16_Name=EARFCN
Columns16_Type=utULInt
Columns17_Name=CellID
Columns17_Type=utULInt
Columns18_Name=PhyCellID
Columns18_Type=utUSInt
"""

        adt_file.write(header_rows_db)