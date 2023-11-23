import os
from sqlalchemy import create_engine, Float, Boolean, Date, MetaData, Table, Integer, String, Column, Text, Time, PrimaryKeyConstraint, ForeignKey, func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
DATABASE_URL = 'postgresql://dastan_kozhabayev_tlb7_user:cxfNP28minTNVy4jsCEqLYd4gf9NoKsX@dpg-clfnap6g1b2c73a2o9c0-a.oregon-postgres.render.com/dastan_kozhabayev_tlb7'
Base = declarative_base()
engine = create_engine(DATABASE_URL)
# mysql+mysqlconnector://root:sacalac2002@localhost:3306/db

# internal
# postgres://dastan_kozhabayev_tlb7_user:cxfNP28minTNVy4jsCEqLYd4gf9NoKsX@dpg-clfnap6g1b2c73a2o9c0-a/dastan_kozhabayev_tlb7

# external
# postgresql://dastan_kozhabayev_tlb7_user:cxfNP28minTNVy4jsCEqLYd4gf9NoKsX@dpg-clfnap6g1b2c73a2o9c0-a.oregon-postgres.render.com/dastan_kozhabayev_tlb7

class User(Base):
    __tablename__ = 'USER'
    user_id = Column(Integer(), primary_key=True)
    email = Column(String(50), nullable=False)
    given_name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
    profile_description = Column(String(200), nullable=False)
    password = Column(String(100), nullable=False)

    caregivers = relationship('Caregiver', backref='User', uselist=False)
    members = relationship('Member', backref='User', uselist=False)

    def __str__(self):
        return f'{self.given_name}'

class Caregiver(Base):
    __tablename__ = 'CAREGIVER'
    caregiver_user_id = Column(Integer(), ForeignKey('USER.user_id', ondelete='CASCADE'), primary_key=True)
    photo = Column(String(100), nullable=False)
    gender = Column(String(1), nullable=False)
    caregiving_type = Column(String(50), nullable=False)
    hourly_rate = Column(Float(), nullable=False)

    job_application = relationship('Job_application', backref='Caregiver')
    appointments = relationship('Appointment', backref='Сaregiver')

    def __repr__(self):
        return f'caregiver id: {self.caregiver_user_id}'



class Member(Base):
    __tablename__ = 'MEMBER'
    member_user_id = Column(Integer(), ForeignKey('USER.user_id', ondelete='CASCADE'), primary_key=True)
    house_rules = Column(String(200), nullable=False)

    address = relationship('Address', backref='Member', uselist=False)
    appointments = relationship('Appointment', backref='Member')
    job = relationship('Job', backref='Member')

    def __repr__(self):
        return f'member id: {self.member_user_id}\nhouse rules: {self.house_rules}'


class Address(Base):
    __tablename__ = 'ADDRESS'
    member_user_id = Column(Integer(), ForeignKey('MEMBER.member_user_id', ondelete='CASCADE'), primary_key=True)
    house_number = Column(String(50), nullable=False)
    street = Column(String(50), nullable=False)
    town = Column(String(50), nullable=False)

    def __repr__(self):
        return 'address'

class Job(Base):
    __tablename__ = 'JOB'
    job_id = Column(Integer(), primary_key=True)
    member_user_id = Column(Integer(), ForeignKey('MEMBER.member_user_id', ondelete='CASCADE'), nullable=False)
    required_caregiving_type = Column(String(250), nullable=False)
    other_requirements = Column(String(250), nullable=False)
    date_posted = Column(Date(), nullable=False)

    def __repr__(self):
        return 'job'

class Job_application(Base):
    __tablename__ = 'JOB_APPLICATION'
    job_id = Column(Integer(), ForeignKey('JOB.job_id', ondelete='CASCADE'), nullable=False)
    caregiver_user_id = Column(Integer(), ForeignKey('CAREGIVER.caregiver_user_id', ondelete='CASCADE'), primary_key=True)
    date_applied = Column(Date(), nullable=False)

    def __repr__(self):
        return 'job_app'

class Appointment(Base):
    __tablename__ = 'APPOINTMENT'
    appointment_id = Column(Integer(), primary_key=True)
    caregiver_user_id = Column(Integer(), ForeignKey('CAREGIVER.caregiver_user_id', ondelete='CASCADE'), nullable=False)
    member_user_id = Column(Integer(), ForeignKey('MEMBER.member_user_id', ondelete='CASCADE'), nullable=False)
    appointment_date = Column(Date(), nullable=False)
    appointment_time = Column(Time(), nullable=False)
    work_hours = Column(Integer(), nullable=False)
    status = Column(Boolean(), nullable=False)

    def __repr__(self):
        return 'appointment'

    









all_caregivers_raw_data = [
{"user_id":1,"email":"kloody0@reuters.com","given_name":"Kermie","surname":"Loody","city":"Żarnów","phone_number":"9594454519","profile_description":"Educated person","password":"dM1>VuWdxYWua", 'photo': 'some url', 'gender': 'F', 'caregiving_type': 'babysitter', 'hourly_rate': 8},
{"user_id":7,"email":"mjuppe6@51.la","given_name":"Mirilla","surname":"Juppe","city":"Ōmiya","phone_number":"9754119114","profile_description":"Ready to work","password":"uP4?Qck|UB\\n", 'photo': 'some url', 'gender': 'F', 'caregiving_type': 'playmate for children', 'hourly_rate': 8},
{"user_id":10,"email":"lfarnan9@reuters.com","given_name":"Linnell","surname":"Farnan","city":"El Olivar","phone_number":"6617590627","profile_description":"I love to work with children","password":"rZ4\"_J&Drn*HS.!", 'photo': 'some url', 'gender': 'F', 'caregiving_type': 'babysitter', 'hourly_rate': 8},
{"user_id":11,"email":"rtroakea@paypal.com","given_name":"Rene","surname":"Troake","city":"Qiryat Shemona","phone_number":"3874652623","profile_description":"I am 20 years old","password":"lK4'OQ'9Kcni5", 'photo': 'some url', 'gender': 'F', 'caregiving_type': 'babysitter', 'hourly_rate': 8},
{"user_id":12,"email":"gskalab@cbc.ca","given_name":"Gaston","surname":"Skala","city":"Asenovgrad","phone_number":"7471211310","profile_description":"I like to play with kids","password":"iM7!=)|g", 'photo': 'some url', 'gender': 'M', 'caregiving_type': 'playmate for children', 'hourly_rate': 100},
{"user_id":14,"email":"bredgewelld@weather.com","given_name":"Brnaba","surname":"Redgewell","city":"Jardín América","phone_number":"8561205136","profile_description":"Graduated nursing school","password":"qR1_\\\\i}_Vsd#o$W", 'photo': 'some url', 'gender': 'M', 'caregiving_type': 'playmate for children', 'hourly_rate': 1},
{"user_id":16,"email":"pstorref@google.es","given_name":"Pryce","surname":"Storre","city":"Mingelchaur","phone_number":"5055887345","profile_description":"I have excellent social skills","password":"tP7+Utt?(Z_f", 'photo': 'some url', 'gender': 'M', 'caregiving_type': 'caregiver for elderly', 'hourly_rate': 145},
{"user_id":17,"email":"fgabelg@cam.ac.uk","given_name":"Franciskus","surname":"Gabel","city":"Huangjin","phone_number":"7825764073","profile_description":"Ready to discuss any topic","password":"mT8,nL\"T6)Qv8", 'photo': 'some url', 'gender': 'M', 'caregiving_type': 'babysitter', 'hourly_rate': 33},
{"user_id":18,"email":"opasekh@typepad.com","given_name":"Ozzy","surname":"Pasek","city":"Yasenevo","phone_number":"2853150258","profile_description":"I can easily handle problematic seniors","password":"jQ4%Av2IXT'G0|>", 'photo': 'some url', 'gender': 'F', 'caregiving_type': 'caregiver for elderly', 'hourly_rate': 56},
{"user_id":20,"email":"wworthingj@ask.com","given_name":"Walker","surname":"Worthing","city":"Águas Vermelhas","phone_number":"8781757730","profile_description":"Already experienced worker","password":"jM9?RU<Y!\\FXc/", 'photo': 'some url', 'gender': 'M', 'caregiving_type': 'caregiver for elderly', 'hourly_rate': 29}
]

caregivers = list()
for caregiver in all_caregivers_raw_data:
    this_user = User(
        user_id = caregiver['user_id'],
        email = caregiver['email'],
        given_name = caregiver['given_name'],
        surname = caregiver['surname'],
        city = caregiver['city'],
        phone_number = caregiver['phone_number'],
        profile_description = caregiver['profile_description'],
        password = caregiver['password']
    )
    caregivers.append(
        Caregiver(
            caregiver_user_id = caregiver['user_id'],
            photo = caregiver['photo'],
            gender = caregiver['gender'],
            caregiving_type = caregiver['caregiving_type'],
            hourly_rate = caregiver['hourly_rate'],
            User = this_user
        )
    )

all_members_raw_data = [
{"user_id":2,"email":"twhaley1@dmoz.org","given_name":"Bolat","surname":"Bolatov","city":"Baixo Guandu","phone_number":"3156694638","profile_description":"","password":"kV0!nMF`~","house_rules": "No pets", "house_number": "some number", "street": "Turan street", "town": "Astana"},
{"user_id":3,"email":"vdoidge2@foxnews.com","given_name":"Viviyan","surname":"Doidge","city":"Palmas De Gran Canaria, Las","phone_number":"7472845950","profile_description":"","password":"hG8@m=QQ}ih","house_rules": "No smoke", "house_number": "some number", "street": "Turan street", "town": "Astana"},
{"user_id":4,"email":"wkopelman3@ehow.com","given_name":"Waverley","surname":"Kopelman","city":"Xiwu","phone_number":"7811661000","profile_description":"","password":"xS3$E#qZ.","house_rules": "No pets", "house_number": "some number", "street": "Turan street", "town": "Astana"},
{"user_id":5,"email":"cboxe4@dagondesign.com","given_name":"Cilka","surname":"Boxe","city":"Tessalit","phone_number":"5232661088","profile_description":"","password":"yL4_ksg5ObLC5J0D","house_rules": "some text", "house_number": "some number", "street": "Turan street", "town": "Astana"},
{"user_id":6,"email":"jweyland5@networkadvertising.org","given_name":"Janetta","surname":"Weyland","city":"Banjar","phone_number":"9767468006","profile_description":"","password":"iQ2'TdbdEJ%MYSH","house_rules": "some text", "house_number": "some number", "street": "some street", "town": "Astana"},
{"user_id":8,"email":"akupper7@free.fr","given_name":"Analiese","surname":"Kupper","city":"Dayong","phone_number":"8481154537","profile_description":"","password":"wZ1{s!\"(","house_rules": "some text", "house_number": "some number", "street": "some street", "town": "Astana"},
{"user_id":9,"email":"josbaldstone8@ameblo.jp","given_name":"Junie","surname":"Osbaldstone","city":"Gongfang","phone_number":"9443019470","profile_description":"","password":"nF2,HT%E`dZcUm","house_rules": "some text", "house_number": "some number", "street": "some street", "town": "Astana"},
{"user_id":13,"email":"kglassc@yahoo.com","given_name":"Kore","surname":"Glass","city":"Anna Regina","phone_number":"2486617238","profile_description":"","password":"jX8#7%}L@_","house_rules": "some text", "house_number": "some number", "street": "some street", "town": "Astana"},
{"user_id":15,"email":"bakame@sohu.com","given_name":"Burk","surname":"Akam","city":"Si Somdet","phone_number":"2794466771","profile_description":"","password":"rO1*b61FRT","house_rules": "some text", "house_number": "some number", "street": "some street", "town": "Astana"},
{"user_id":19,"email":"gsallengeri@cloudflare.com","given_name":"Gawain","surname":"Sallenger","city":"Kamensk-Ural’skiy","phone_number":"3026034007","profile_description":"","password":"tN5$+blfr+C","house_rules": "some text", "house_number": "some number", "street": "some street", "town": "Astana"},
]
members = list()
for member in all_members_raw_data:
    this_user = User(
        user_id = member['user_id'],
        email = member['email'],
        given_name = member['given_name'],
        surname = member['surname'],
        city = member['city'],
        phone_number = member['phone_number'],
        profile_description = member['profile_description'],
        password = member['password']
    )
    this_address = Address(
        member_user_id = member['user_id'],
        house_number = member['house_number'],
        street = member['street'],
        town = member['town']
    )
    members.append(
        Member(
            member_user_id = member['user_id'],
            house_rules = member['house_rules'],
            User = this_user,
            address = this_address
        )
    )


jobs = list()
jobs.append(Job(job_id = 1, member_user_id = members[0].member_user_id, required_caregiving_type = 'babysitter', other_requirements = 'gentle', date_posted = '2023-11-18'))
jobs.append(Job(job_id = 2, member_user_id = members[1].member_user_id, required_caregiving_type = 'playmate for children', other_requirements = 'no smoke', date_posted = '2023-11-18'))
jobs.append(Job(job_id = 3, member_user_id = members[2].member_user_id, required_caregiving_type = 'babysitter', other_requirements = 'gentle', date_posted = '2023-11-18'))
jobs.append(Job(job_id = 4, member_user_id = members[3].member_user_id, required_caregiving_type = 'babysitter', other_requirements = 'play educational games', date_posted = '2023-11-18'))
jobs.append(Job(job_id = 5, member_user_id = members[4].member_user_id, required_caregiving_type = 'playmate for children', other_requirements = 'go outside with kids', date_posted = '2023-11-18'))
jobs.append(Job(job_id = 6, member_user_id = members[5].member_user_id, required_caregiving_type = 'playmate for children', other_requirements = 'no preferences', date_posted = '2023-11-18'))
jobs.append(Job(job_id = 7, member_user_id = members[6].member_user_id, required_caregiving_type = 'caregiver for elderly', other_requirements = 'my dad loves discussion', date_posted = '2023-11-18'))
jobs.append(Job(job_id = 8, member_user_id = members[7].member_user_id, required_caregiving_type = 'babysitter', other_requirements = 'want to hire a person for a long time period', date_posted = '2023-11-18'))
jobs.append(Job(job_id = 9, member_user_id = members[8].member_user_id, required_caregiving_type = 'caregiver for elderly people', other_requirements = 'no prefences', date_posted = '2023-11-18'))
jobs.append(Job(job_id = 10, member_user_id = members[9].member_user_id, required_caregiving_type = 'caregiver for elderly people', other_requirements = 'only for the summer period', date_posted = '2023-11-18'))



job_applications = list()
job_applications.append(Job_application(caregiver_user_id = caregivers[0].caregiver_user_id, job_id = jobs[0].job_id, date_applied = '2023-11-18'))
job_applications.append(Job_application(caregiver_user_id = caregivers[1].caregiver_user_id, job_id = jobs[1].job_id, date_applied = '2023-11-18'))
job_applications.append(Job_application(caregiver_user_id = caregivers[2].caregiver_user_id, job_id = jobs[2].job_id, date_applied = '2023-11-18'))
job_applications.append(Job_application(caregiver_user_id = caregivers[3].caregiver_user_id, job_id = jobs[3].job_id, date_applied = '2023-11-18'))
job_applications.append(Job_application(caregiver_user_id = caregivers[4].caregiver_user_id, job_id = jobs[4].job_id, date_applied = '2023-11-18'))
job_applications.append(Job_application(caregiver_user_id = caregivers[5].caregiver_user_id, job_id = jobs[5].job_id, date_applied = '2023-11-18'))
job_applications.append(Job_application(caregiver_user_id = caregivers[6].caregiver_user_id, job_id = jobs[6].job_id, date_applied = '2023-11-18'))
job_applications.append(Job_application(caregiver_user_id = caregivers[7].caregiver_user_id, job_id = jobs[7].job_id, date_applied = '2023-11-18'))
job_applications.append(Job_application(caregiver_user_id = caregivers[8].caregiver_user_id, job_id = jobs[8].job_id, date_applied = '2023-11-18'))
job_applications.append(Job_application(caregiver_user_id = caregivers[9].caregiver_user_id, job_id = jobs[9].job_id, date_applied = '2023-11-18'))


def create_appointment(caregiver, member, appointment_date, appointment_time, work_hours):
    return Appointment(
        appointment_id = caregiver.caregiver_user_id + member.member_user_id,
        caregiver_user_id = caregiver.caregiver_user_id,
        member_user_id = member.member_user_id,
        appointment_date = appointment_date,
        appointment_time = appointment_time,
        work_hours = work_hours,
        status = (caregiver.caregiving_type == member.job.required_caregiving_type)
    )
appointments = list()
appointments.append(Appointment(appointment_id = 1, caregiver_user_id = caregivers[0].caregiver_user_id, member_user_id = members[0].member_user_id, appointment_date = '2023-11-18', appointment_time = '19:00', work_hours = 1, status = True))
appointments.append(Appointment(appointment_id = 2, caregiver_user_id = caregivers[1].caregiver_user_id, member_user_id = members[1].member_user_id, appointment_date = '2023-11-18', appointment_time = '19:00', work_hours = 2, status = True))
appointments.append(Appointment(appointment_id = 3, caregiver_user_id = caregivers[2].caregiver_user_id, member_user_id = members[2].member_user_id, appointment_date = '2023-11-18', appointment_time = '19:00', work_hours = 3, status = True))
appointments.append(Appointment(appointment_id = 4, caregiver_user_id = caregivers[3].caregiver_user_id, member_user_id = members[3].member_user_id, appointment_date = '2023-11-18', appointment_time = '19:00', work_hours = 4, status = True))
appointments.append(Appointment(appointment_id = 5, caregiver_user_id = caregivers[4].caregiver_user_id, member_user_id = members[4].member_user_id, appointment_date = '2023-11-18', appointment_time = '19:00', work_hours = 5, status = True))
appointments.append(Appointment(appointment_id = 6, caregiver_user_id = caregivers[5].caregiver_user_id, member_user_id = members[5].member_user_id, appointment_date = '2023-11-18', appointment_time = '19:00', work_hours = 6, status = False))
appointments.append(Appointment(appointment_id = 7, caregiver_user_id = caregivers[6].caregiver_user_id, member_user_id = members[6].member_user_id, appointment_date = '2023-11-18', appointment_time = '19:00', work_hours = 7, status = False))
appointments.append(Appointment(appointment_id = 8, caregiver_user_id = caregivers[7].caregiver_user_id, member_user_id = members[7].member_user_id, appointment_date = '2023-11-18', appointment_time = '19:00', work_hours = 8, status = False))
appointments.append(Appointment(appointment_id = 9, caregiver_user_id = caregivers[8].caregiver_user_id, member_user_id = members[8].member_user_id, appointment_date = '2023-11-18', appointment_time = '19:00', work_hours = 9, status = False))
appointments.append(Appointment(appointment_id = 10, caregiver_user_id = caregivers[9].caregiver_user_id, member_user_id = members[9].member_user_id, appointment_date = '2023-11-18', appointment_time = '19:00', work_hours = 10, status = False))



Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()

# for caregiver in caregivers:
#     session.add(caregiver)
#     session.commit()

# for member in members:
#     session.add(member)
#     session.commit()

# for job in jobs:
#     session.add(job)
#     session.commit()

# for job_application in job_applications:
#     session.add(job_application)
#     session.commit()

# for appointment in appointments:
#     session.add(appointment)
#     session.commit()

print('hello world')
