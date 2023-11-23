from flask import Flask, render_template, url_for, request, redirect
from db import session, User, Caregiver, Member, Address, Job, Job_application, Appointment, func

app = Flask(__name__)


@app.route('/')
def index():
    users = session.query(User).order_by(User.user_id).all()
    members = session.query(Member).order_by(Member.member_user_id).all()
    caregivers = session.query(Caregiver).order_by(Caregiver.caregiver_user_id).all()
    return render_template('index.html', users=users, members=members, caregivers=caregivers)

@app.route('/info/<int:id>/delete')
def delete(id):
    user = session.query(User).filter(User.user_id == id)
    try:
        user.delete()
        session.commit()
        return redirect('/')
    except:
        return 'An error occured during deleting the user'

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    user = session.query(User).filter(User.user_id == id).first()
    member = session.query(Member).filter(Member.member_user_id == id).first()
    caregiver = session.query(Caregiver).filter(Caregiver.caregiver_user_id == id).first()
    member_appointment = session.query(Appointment).filter(Appointment.member_user_id == id).first()
    caregiver_appointment = session.query(Appointment).filter(Appointment.caregiver_user_id == id).first()
    job = session.query(Job).filter(Job.member_user_id == id).first()
    address = session.query(Address).filter(Address.member_user_id == id).first()
    job_application = session.query(Job_application).filter(Job_application.caregiver_user_id == id).first()

    if request.method == 'POST':
        # UPDATING USER
        user.given_name = request.form['given_name']
        user.surname = request.form['surname']
        user.email = request.form['email']
        user.city = request.form['city']
        user.phone_number = request.form['phone_number']
        user.profile_description = request.form['profile_description']
        user.password = request.form['password']
        if member != None:
            # UPDATING MEMBER ADDRESS
            address.house_number = request.form['house_number']
            address.street = request.form['street']
            address.town = request.form['town']

            # UPDATING MEMBER
            member.house_rules = request.form['house_rules']

            # UPDATING MEMBER JOB
            if job != None:
                job.other_requirements = request.form['other_requirements']
                job.required_caregiving_type = request.form['required_caregiving_type']
            else:
                this_job = Job (
                    member_user_id = member.member_user_id,
                    required_caregiving_type = request.form['required_caregiving_type'],
                    other_requirements = request.form['other_requirements'],
                    date_posted = '2023-11-18'
                )
                member.job.append(this_job)

            # UPDATING MEMBER APPOINTMENT
            selected_status = request.form.get('status')
            if member_appointment != None:
                if selected_status == 'True':
                    member_appointment.status = 1
                else:
                    member_appointment.status = 0
            else:
                random_caregiver = session.query(Caregiver).first()
                this_appointment = Appointment(
                    caregiver_user_id = random_caregiver.caregiver_user_id,
                    member_user_id = member.member_user_id,
                    appointment_date = '2023-11-18',
                    appointment_time = '18:00',
                    work_hours = 4,
                    status = 1 
                )
                member.appointments.append(this_appointment)

            try:
                session.commit()
                return redirect('/')
            except:
                return f'An error occured during editing the member, random caregiver id: {random_caregiver.caregiver_user_id}'
        else:
            # UPDATING CAREGIVER 
            selected_gender = request.form.get('gender')
            caregiver.gender = selected_gender
            selected_caregiving_type = request.form.get('caregiving_type')
            caregiver.caregiving_type = selected_caregiving_type
            caregiver.hourly_rate = request.form['hourly_rate']

            # UPDATING CAREGIVER APPOINTMENT IF IT EXISTS
            selected_status = request.form.get('status')
            if caregiver_appointment != None:
                if selected_status == 'True':
                    print('\n\n\n\n\n\nstatus is true\n\n\n\n\n\n')
                    caregiver_appointment.status = 1
                if selected_status == 'False':
                    print('\n\n\n\n\n\nstatus is false\n\n\n\n\n\n')
                    caregiver_appointment.status = 0
                else:
                    print('\n\n\n\n\n\nLOOOL\n\n\n\n\n\n')
            else:
                random_member = session.query(Member).first()
                this_appointment = Appointment(
                    caregiver_user_id = caregiver.caregiver_user_id,
                    member_user_id = random_member.member_user_id,
                    appointment_date = '2023-11-18',
                    appointment_time = '18:00',
                    work_hours = 4,
                    status = 1 
                )
                print('\n\n\n\n\n\nDAAAAUN\n\n\n\n\n\n')
                caregiver.appointments.append(this_appointment)

            try:
                session.commit()
                return redirect('/')
            except:
                return 'An error occured during editing the caregiver'
    else:
        if member != None:
            return render_template('edit_member.html', user=user, member=member, job=job, address=address, appointment=member_appointment)
        else:
            return render_template('edit_caregiver.html', caregiver=caregiver, user=user, job_application=job_application, appointment=caregiver_appointment)


@app.route('/info/<int:id>')
def info(id):
    user = session.query(User).filter(User.user_id == id).first()
    member = session.query(Member).filter(Member.member_user_id == id).first()
    caregiver = session.query(Caregiver).filter(Caregiver.caregiver_user_id == id).first()
    member_appointment = session.query(Appointment).filter(Appointment.member_user_id == id).first()
    caregiver_appointment = session.query(Appointment).filter(Appointment.caregiver_user_id == id).first()
    if member != None:
        job = session.query(Job).filter(Job.member_user_id == id).first()
        address = session.query(Address).filter(Address.member_user_id == id).first()
        return render_template('info_member.html', member=member, user=user, address=address, appointment=member_appointment, job=job)
    else:
        job_application = session.query(Job_application).filter(Job_application.caregiver_user_id == id).first()
        return render_template('info_caregiver.html', caregiver=caregiver, user=user, job_application=job_application, appointment=caregiver_appointment)

@app.route('/create_caregiver', methods=['POST', 'GET'])
def create_caregiver():
    if request.method == 'POST':
        this_user = User(
            given_name = request.form['given_name'],
            surname = request.form['surname'],
            email = request.form['email'],
            city = request.form['city'],
            phone_number = request.form['phone_number'],
            profile_description = request.form['profile_description'],
            password = request.form['password']
        )
        selected_caregiving_type = request.form.get('caregiving_type')
        selected_gender = request.form.get('gender')
        selected_photo = 'some url'
        this_caregiver = Caregiver(
            photo = selected_photo,
            gender = selected_gender,
            caregiving_type = selected_caregiving_type,
            hourly_rate = request.form['hourly_rate'],
            User = this_user
        )
        
        try:
            session.add(this_caregiver)
            session.commit()
            return redirect('/')
        except:
            return 'An error occured during creating a new user'
    else:
        return render_template('create_caregiver.html')
    

@app.route('/create_member', methods=['POST', 'GET'])
def create_member():
    if request.method == 'POST':
        this_user = User(
            given_name = request.form['given_name'],
            surname = request.form['surname'],
            email = request.form['email'],
            city = request.form['city'],
            phone_number = request.form['phone_number'],
            profile_description = request.form['profile_description'],
            password = request.form['password']
        )
        
        this_address = Address(
            house_number = request.form['house_number'],
            street = request.form['street'],
            town = request.form['town']
        )

        this_member = Member(
            house_rules = request.form['house_rules'],
            User = this_user,
            address = this_address
        )
        
        try:
            session.add(this_member)
            session.commit()
            return redirect('/')
        except:
            return 'An error occured'
    else:
        return render_template('create_member.html')


if __name__ == '__main__':
    app.run(debug=True)