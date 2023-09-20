from dataclasses import dataclass


@dataclass
class Applicant:
    code: str
    phone: str
    email: str
    login: str
    password_email: str
    password_vfs: str
    travel_date: str
    first_name: str
    last_name: str
    birth_date: str
    passport_no: str
    issue_date: str
    exp_date: str
    issue_place: str
    gender: str
    travel_start: str
    travel_end: str


test_user = Applicant(
    '7',
    '9252090883',
    # 'VANELI@YANDEX.RU',
    'INTCHERNOV@YANDEX.RU',
    'Vaneli',
    '240297-',
    '240297Vis@',
    '2023-10-27',
    'IVAN',
    'KRASNOV',
    # '03/30/1996',
    '30031996',
    '732842880',
    '2014-05-16',
    # '05/16/2024',
    '16052024',
    'FMS34001',
    'Male',
    '01112023',
    '10112023'
)
