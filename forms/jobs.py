from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, TextAreaField, StringField, BooleanField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = IntegerField('ID Руководителя', validators=[DataRequired()])
    job = TextAreaField('Описание работы')
    work_size = IntegerField('Объем работы в часах', validators=[DataRequired()])
    collaborators = StringField('Список ID участников через запятую', validators=[DataRequired()])
    is_finished = BooleanField('Выполнена ли работа?')
    submit = SubmitField('Создать')
