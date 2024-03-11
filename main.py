import argparse
from datetime import datetime

from pprint import pprint

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--action', dest='action', help='Action: create/list/update/remove')
parser.add_argument('-m', '--model', dest='model', help='Model: Teacher/Student/Group/Discipline')
parser.add_argument('-n', '--name', dest='name', help='Name of Teacher/Student/Group/Discipline')
parser.add_argument('--id', dest='id', help='ID of Teacher/Student/Group/Discipline')
parser.add_argument('--gr_id', dest='group_id', help='Group ID')
parser.add_argument('--t_id', dest='teacher_id', help='Teacher ID')
parser.add_argument('-g', '--grade', dest='grade', help='Grade')
parser.add_argument('--st_id', dest='student_id', help='Student ID')
parser.add_argument('--d_id', dest='discipline_id', help='Discipline ID')

args = parser.parse_args()


def create(model: str, name: str, grade=None, group_id=None, teacher_id=None, student_id=None, discipline_id=None):

    match model:

        case 'Teacher':
            teacher = Teacher(fullname=name)
            session.add(teacher)

        case 'Student':
            student = Student(fullname=name, group_id=group_id)
            session.add(student)

        case 'Group':
            group = Group(name=name)
            session.add(group)

        case 'Discipline':
            discipline = Discipline(name=name, teacher_id=teacher_id)
            session.add(discipline)

        case 'Grade':
            grade_ = Grade(grade=grade, date_of=datetime.strftime(datetime.now().date(), '%Y-%m-%d'), student_id=student_id, discipline_id=discipline_id)
            session.add(grade_)

    session.commit()
    return 'The operation was completed successfully'


def list_(model:str):
    
    match model:

        case 'Teacher':
            result = session.query(Teacher.fullname).select_from(Teacher).all()

        case 'Student':
            result = session.query(Student.fullname).select_from(Student).all()

        case 'Group':
            result = session.query(Group.name).select_from(Group).all()

        case 'Discipline':
            result = session.query(Discipline.name).select_from(Discipline).all()

        case 'Grade':
            result = session.query(Grade.grade).select_from(Grade).all()

    return result


def update(model: str, id:int, name:str):
    
    match model:

        case 'Teacher':
            new_info = session.query(Teacher).filter(Teacher.id == id)
            if new_info:
                new_info.update({'fullname': name})
                session.commit()

        case 'Student':
            new_info = session.query(Student).filter(Student.id == id)
            if new_info:
                new_info.update({'fullname': name})
                session.commit()

        case 'Group':
            new_info = session.query(Group).filter(Group.id == id)
            if new_info:
                new_info.update({'name': name})
                session.commit()

        case 'Discipline':
            new_info = session.query(Discipline).filter(Discipline.id == id)
            if new_info:
                new_info.update({'name': name})
                session.commit()

    return 'The operation was completed successfully'


def remove(model: str, id: int):
        
    match model:

        case 'Teacher':
            session.query(Teacher).filter(Teacher.id == id).delete()
            session.commit()

        case 'Student':
            session.query(Student).filter(Student.id == id).delete()
            session.commit()

        case 'Group':
            session.query(Group).filter(Group.id == id).delete()
            session.commit()

        case 'Discipline':
            session.query(Discipline).filter(Discipline.id == id).delete()
            session.commit()

        case 'Grade':
            session.query(Grade).filter(Grade.id == id).delete()
            session.commit()

    return 'The operation was completed successfully'


def main():

    match args.action:

        case 'create':
            print(create(args.model, args.name, group_id=args.group_id, teacher_id=args.teacher_id, grade=args.grade, student_id=args.student_id, discipline_id=args.discipline_id))

        case 'list':
            pprint(list_(args.model))

        case 'update':
            print(update(args.model, args.id, args.name))

        case 'remove':
            print(remove(args.model, args.id))

        case _:
            print('No operation')


if __name__ == '__main__':
    main()