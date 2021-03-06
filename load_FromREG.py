# -*- coding: utf-8 -*-

import arcpy as a
from os import path
from sys import exit


input_fcs = a.GetParameterAsText(0)
taxationDB = a.GetParameterAsText(1)
cleanDB = a.GetParameter(2)

SOATO_to_ADMR_dict = {
    "1204000000": (104, u"БАРАНОВИЧСКИЙ"),
    "1208000000": (108, u"БЕРЁЗОВСКИЙ"),
    "1212000000": (112, u"БРЕСТСКИЙ"),
    "1216000000": (116, u"ГАНЦЕВИЧСКИЙ"),
    "1220000000": (120, u"ДРОГИЧИНСКИЙ"),
    "1225000000": (125, u"ЖАБИНКОВСКИЙ"),
    "1230000000": (130, u"ИВАНОВСКИЙ"),
    "1234000000": (134, u"ИВАЦЕВИЧСКИЙ"),
    "1240000000": (140, u"КАМЕНЕЦКИЙ"),
    "1243000000": (143, u"КОБРИНСКИЙ"),
    "1243501000": (713, u"г. Кобрин"),
    "1247000000": (147, u"ЛУНИНЕЦКИЙ"),
    "1247501000": (714, u"г. Лунинец"),
    "1250000000": (150, u"ЛЯХОВИЧСКИЙ"),
    "1252000000": (152, u"МАЛОРИТСКИЙ"),
    "1254000000": (154, u"ПИНСКИЙ"),
    "1256000000": (156, u"ПРУЖАНСКИЙ"),
    "1258000000": (158, u"СТОЛИНСКИЙ"),
    "1401000000": (711, u"г. Брест"),
    "1410000000": (712, u"г. Барановичи"),
    "1445000000": (715, u"г. Пинск"),
    "2205000000": (205, u"БЕШЕНКОВИЧСКИЙ"),
    "2208000000": (208, u"БРАСЛАВСКИЙ"),
    "2210000000": (210, u"ВЕРХНЕДВИНСКИЙ"),
    "2212000000": (212, u"ВИТЕБСКИЙ"),
    "2215000000": (215, u"ГЛУБОКСКИЙ"),
    "2218000000": (218, u"ГОРОДОКСКИЙ"),
    "2221000000": (221, u"ДОКШИЦКИЙ"),
    "2224000000": (224, u"ДУБРОВЕНСКИЙ"),
    "2227000000": (227, u"ЛЕПЕЛЬСКИЙ"),
    "2227501000": (722, u"г. Лепель"),
    "2230000000": (230, u"ЛИОЗНЕНСКИЙ"),
    "2233000000": (233, u"МИОРСКИЙ"),
    "2236000000": (236, u"ОРШАНСКИЙ"),
    "2236501000": (724, u"г. Орша"),
    "2238000000": (238, u"ПОЛОЦКИЙ"),
    "2238501000": (725, u"г. Полоцк"),
    "2240000000": (240, u"ПОСТАВСКИЙ"),
    "2242000000": (242, u"РОССОНСКИЙ"),
    "2244000000": (244, u"СЕННЕНСКИЙ"),
    "2246000000": (246, u"ТОЛОЧИНСКИЙ"),
    "2249000000": (249, u"УШАЧСКИЙ"),
    "2251000000": (251, u"ЧАШНИКСКИЙ"),
    "2255000000": (255, u"ШАРКОВЩИНСКИЙ"),
    "2258000000": (258, u"ШУМИЛИНСКИЙ"),
    "2401000000": (721, u"г. Витебск"),
    "2418000000": (723, u"г. Новополоцк"),
    "3203000000": (303, u"БРАГИНСКИЙ"),
    "3205000000": (305, u"БУДА-КОШЕЛЁВСКИЙ"),
    "3208000000": (308, u"ВЕТКОВСКИЙ"),
    "3210000000": (310, u"ГОМЕЛЬСКИЙ"),
    "3212000000": (312, u"ДОБРУШСКИЙ"),
    "3212501000": (732, u"г. Добруш"),
    "3214000000": (314, u"ЕЛЬСКИЙ"),
    "3216000000": (316, u"ЖИТКОВИЧСКИЙ"),
    "3218000000": (318, u"ЖЛОБИНСКИЙ"),
    "3218501000": (733, u"г. Жлобин"),
    "3223000000": (323, u"КАЛИНКОВИЧСКИЙ"),
    "3223501000": (734, u"г. Калинковичи"),
    "3225000000": (325, u"КОРМЯНСКИЙ"),
    "3228000000": (328, u"ЛЕЛЬЧИЦКИЙ"),
    "3230000000": (330, u"ЛОЕВСКИЙ"),
    "3235000000": (335, u"МОЗЫРСКИЙ"),
    "3235501000": (735, u"г. Мозырь"),
    "3238000000": (338, u"НАРОВЛЯНСКИЙ"),
    "3240000000": (340, u"ОКТЯБРЬСКИЙ"),
    "3243000000": (343, u"ПЕТРИКОВСКИЙ"),
    "3245000000": (345, u"РЕЧИЦКИЙ"),
    "3245501000": (736, u"г. Речица"),
    "3247000000": (347, u"РОГАЧЁВСКИЙ"),
    "3247501000": (737, u"г. Рогачёв"),
    "3250000000": (350, u"СВЕТЛОГОРСКИЙ"),
    "3250501000": (738, u"г. Светлогорск"),
    "3254000000": (354, u"ХОЙНИКСКИЙ"),
    "3256000000": (356, u"ЧЕЧЕРСКИЙ"),
    "3401000000": (731, u"г. Гомель"),
    "4204000000": (404, u"БЕРЕСТОВИЦКИЙ"),
    "4208000000": (408, u"ВОЛКОВЫССКИЙ"),
    "4208501000": (742, u"г. Волковыск"),
    "4213000000": (413, u"ВОРОНОВСКИЙ"),
    "4220000000": (420, u"ГРОДНЕНСКИЙ"),
    "4223000000": (423, u"ДЯТЛОВСКИЙ"),
    "4226000000": (426, u"ЗЕЛЬВЕНСКИЙ"),
    "4229000000": (429, u"ИВЬЕВСКИЙ"),
    "4233000000": (433, u"КОРЕЛИЧСКИЙ"),
    "4236000000": (436, u"ЛИДСКИЙ"),
    "4236501000": (743, u"г. Лида"),
    "4240000000": (440, u"МОСТОВСКИЙ"),
    "4243000000": (443, u"НОВОГРУДСКИЙ"),
    "4243501000": (744, u"г. Новогрудок"),
    "4246000000": (446, u"ОСТРОВЕЦКИЙ"),
    "4249000000": (449, u"ОШМЯНСКИЙ"),
    "4252000000": (452, u"СВИСЛОЧСКИЙ"),
    "4254000000": (454, u"СЛОНИМСКИЙ"),
    "4254501000": (745, u"г. Слоним"),
    "4256000000": (456, u"СМОРГОНСКИЙ"),
    "4258000000": (458, u"ЩУЧИНСКИЙ"),
    "4401000000": (741, u"г. Гродно"),
    "5000000000": (751, u"г. Минск"),
    "6204000000": (504, u"БЕРЕЗИНСКИЙ"),
    "6208000000": (508, u"БОРИСОВСКИЙ"),
    "6208501000": (752, u"г. Борисов"),
    "6213000000": (513, u"ВИЛЕЙСКИЙ"),
    "6213501000": (753, u"г. Вилейка"),
    "6220000000": (520, u"ВОЛОЖИНСКИЙ"),
    "6222000000": (522, u"ДЗЕРЖИНСКИЙ"),
    "6222501000": (754, u"г. Дзержинск"),
    "6225000000": (525, u"КЛЕЦКИЙ"),
    "6228000000": (528, u"КОПЫЛЬСКИЙ"),
    "6230000000": (530, u"КРУПСКИЙ"),
    "6232000000": (532, u"ЛОГОЙСКИЙ"),
    "6234000000": (534, u"ЛЮБАНСКИЙ"),
    "6236000000": (536, u"МИНСКИЙ"),
    "6238000000": (538, u"МОЛОДЕЧНЕНСКИЙ"),
    "6238501000": (756, u"г. Молодечно"),
    "6240000000": (540, u"МЯДЕЛЬСКИЙ"),
    "6242000000": (542, u"НЕСВИЖСКИЙ"),
    "6244000000": (544, u"ПУХОВИЧСКИЙ"),
    "6246000000": (546, u"СЛУЦКИЙ"),
    "6246501000": (757, u"г. Слуцк"),
    "6248000000": (548, u"СМОЛЕВИЧСКИЙ"),
    "6250000000": (550, u"СОЛИГОРСКИЙ"),
    "6250501000": (758, u"г. Солигорск"),
    "6252000000": (552, u"СТАРОДОРОЖСКИЙ"),
    "6254000000": (554, u"СТОЛБЦОВСКИЙ"),
    "6256000000": (556, u"УЗДЕНСКИЙ"),
    "6258000000": (558, u"ЧЕРВЕНСКИЙ"),
    "6413000000": (755, u"г. Жодино"),
    "7204000000": (604, u"БЕЛЫНИЧСКИЙ"),
    "7208000000": (608, u"БОБРУЙСКИЙ"),
    "7213000000": (613, u"БЫХОВСКИЙ"),
    "7217000000": (617, u"ГЛУССКИЙ"),
    "7220000000": (620, u"ГОРЕЦКИЙ"),
    "7220501000": (763, u"г. Горки"),
    "7223000000": (660, u"ДРИБИНСКИЙ"),
    "7225000000": (625, u"КИРОВСКИЙ"),
    "7228000000": (628, u"КЛИМОВИЧСКИЙ"),
    "7230000000": (630, u"КЛИЧЕВСКИЙ"),
    "7235000000": (635, u"КОСТЮКОВИЧСКИЙ"),
    "7238000000": (638, u"КРАСНОПОЛЬСКИЙ"),
    "7240000000": (640, u"КРИЧЕВСКИЙ"),
    "7240501000": (764, u"г. Кричев"),
    "7242000000": (642, u"КРУГЛЯНСКИЙ"),
    "7244000000": (644, u"МОГИЛЁВСКИЙ"),
    "7246000000": (646, u"МСТИСЛАВСКИЙ"),
    "7248000000": (648, u"ОСИПОВИЧСКИЙ"),
    "7248501000": (765, u"г. Осиповичи"),
    "7250000000": (650, u"СЛАВГОРОДСКИЙ"),
    "7252000000": (652, u"ХОТИМСКИЙ"),
    "7254000000": (654, u"ЧАУССКИЙ"),
    "7256000000": (656, u"ЧЕРИКОВСКИЙ"),
    "7258000000": (658, u"ШКЛОВСКИЙ"),
    "7401000000": (761, u"г. Могилев"),
    "7410000000": (762, u"г. Бобруйск")
    }

fcs_list = input_fcs.replace("'", "").split(';')
LotsREG = path.join(taxationDB, u"BORDERS", u"LotsReg")

project_name = path.basename(path.dirname(taxationDB))
if project_name[:7] == u"Лесхоз_":
    leshoz_number = project_name.split('_')[1].replace(' ', '')
elif project_name.split(' ')[1][:7] == u"Лесхоз_":
    leshoz_number = project_name.split(' ')[1].split('_')[1]
else:
    a.AddWarning(u"Неизвестный формат названия папки с проектом лесоустройства")
    exit()

if cleanDB:
    try:
        a.TruncateTable_management(LotsREG)
        a.AddMessage(u"Прежние сведения о регистрации земельных участков успешно удалены из таблицы!")
    except:
        a.AddWarning(u"Не удалось удалить сведения о регистрации из Borders\\LotsREG")
        exit()

a.AddMessage(u"Добавление данных о регистрации земельных участков в базу")
try:       
    fms = a.FieldMappings()
    for LotsREG_field in ["CADNUM", "ADDRESS","PURPOSE","SQ","DATEREG","UNAME_1"]:
        fm = a.FieldMap()
        for fc in fcs_list:
            fields = {}
            for f in a.ListFields(fc):
                fields[f.name.upper()] = f
            if LotsREG_field in fields:
                fm.addInputField(fc, LotsREG_field)
        x = fm.outputField
        x.name = LotsREG_field
        fm.outputField = x
        fms.addFieldMap(fm)

    a.Append_management(inputs=input_fcs, target=LotsREG, 
                        schema_type="NO_TEST", field_mapping=fms, subtype="")
    a.CalculateField_management (in_table=LotsREG, field='LESHOZKOD', 
                                 expression=leshoz_number)

    with a.da.UpdateCursor(LotsREG, ["CADNUM", "ADMR"]) as cursor:
        for row in cursor:
            row[1] = str(SOATO_to_ADMR_dict[row[0][:4] + "000000"][0])
            cursor.updateRow(row)
    del cursor

    a.AddMessage('Загрузка регистрации завершена успешно!')
except:
    a.AddWarning(u"Загрузка не завершена!")
