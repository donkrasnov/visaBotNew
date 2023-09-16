from dataclasses import dataclass


@dataclass
class Applicant:
    phone: str
    email: str
    login: str
    password: str
    travel_date: str
    first_name: str
    last_name: str
    birth_date: str
    passport_no: str
    issue_date: str
    exp_date: str
    issue_place: str


# olesia = Applicant(
#     '9951124802',
#     'oless1a@yandex.ru',
#     'oless1a',
#     'Vizaisp',
#     '2023-09-30',
#     'Olesia',
#     'Orlova',
#     '1997-07-25',
#     '664777884',
#     '2023-04-28',
#     '2028-04-28',
#     'MVD0141'
# )

# sayana = Applicant(
#     '9153951803',
#     'ssayana2022@yandex.ru',
#     'ssayana2022',
#     'Open2022ss',
#     '2023-11-01',
#     'Sayana',
#     'Sanzhimitupova',
#     '1986-07-06',
#     '758651373',
#     '2018-07-26',
#     '2028-07-26',
#     'MVD77315'
# )

# Normal only
anzorov = Applicant(
    '9036838800',
    'Anzoro8@yandex.ru',
    'Anzoro8',
    'anzorro08',
    '2023-10-16',
    'ALAN',
    'ANZOROV',
    '1978-08-11',
    '753553727',
    '2016-08-28',
    '2026-08-28',
    'FMS2001'
)

# saxonova = Applicant(
#     '9104604968',
#     'saxonovalud@yandex.ru',
#     'saxonovalud',
#     'Dunat1+',
#     '2023-12-07',
#     'Liudmila',
#     'Saksonova',
#     '1949-12-10',
#     '761168435',
#     '2019-07-23',
#     '2029-07-23',
#     'MVD77432'
# )

mariia = Applicant(
    '9958854737',
    'gate.mari603@yandex.ru',
    'gate.mari603',
    'Gatemari603',
    '2023-10-30',
    'Mariia',
    'Litvinova',
    '1993-03-06',
    '769059410',
    '2022-10-21',
    '2032-10-21',
    'MVD77612'
)

nadezhda = Applicant(
    '9519029074',
    'nadesdann@yandex.ru',
    'nadesdann',
    'Yflt;lf1979',
    '2024-02-03',
    'Nadezhda',
    'Toropova',
    '1979-06-09',
    '758067005',
    '2018-06-06',
    '2028-06-06',
    'MVD52015'
)

katerina = Applicant(
    '9854150914',
    'intchernov@yandex.ru',
    'intchernov',
    '240297-',
    '2023-12-03',
    'Katerina',
    'Shovkrinskaia',
    '1976-09-04',
    '762802665',
    '2020-03-13',
    '2030-03-13',
    'MVD50003'
)