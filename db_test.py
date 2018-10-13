from model import *
from app import db


admin = Role(name='Admin')
call = Role(name='Call Operator')
gov = Role(name='Government Agency')

at = User(username='admin_test', password='admin_test', role_id=1)
ct = User(username='call_operator_test', password='call_operator_test', role_id=2)
gt = User(username='government_agency_test', password='government_agency_test', role_id=3)

db.session.add(admin)
db.session.add(call)
db.session.add(gov)

db.session.add(at)
db.session.add(ct)
db.session.add(gt)

db.session.commit()