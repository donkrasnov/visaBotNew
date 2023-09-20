from dataclasses import dataclass


@dataclass
class Applicant:
    code: str
    phone: str
    login_email: str
    email: str
    password_vfs: str
    first_name: str
    last_name: str
    birth_date: str
    passport_no: str
    exp_date: str
    issue_place: str
    gender: str


test_user = Applicant(
    '7',
    '9252090883',
    # 'INTCHERNOV@YANDEX.RU'
    'VANELI@YANDEX.RU',
    'VANELI@YANDEX.RU',
    '240297Vis@',
    'IVAN',
    'KRASNOV',
    '30031996',
    '732842880',
    '16052024',
    'FMS34001',
    'Male',
)


test_user_2 = Applicant(
    '7',
    '9252101020',
    'VANELI@YANDEX.RU',
    'VAN321@BK.RU',
    '240297Vis@',
    'IVAN',
    'KRASNOV',
    '23031996',
    '732882881',
    '18072026',
    'FMS34003',
    'Male',
)
