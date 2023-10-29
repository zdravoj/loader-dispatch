from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class HomeForm(FlaskForm):
    loaders_num = IntegerField(
        'Number of Loaders to Assign:',
        validators= [
            DataRequired(),
            NumberRange(1, 20, 'The number of loaders must be between 1 and 20')
        ],
        render_kw={'id':'loaders_num'}
    )
    doors_num = IntegerField(
        'Number of Doors to Assign:',
        validators=[
            DataRequired(),
            NumberRange(1, 80, 'The number of doors must be between 1 and 80')
        ],
        render_kw={'id':'doors_num'}
    )
    start_door_num = IntegerField(
        'Starting Door Number:',
        validators=[
            DataRequired(),
            NumberRange(0, 1000, 'The starting door number must be between 0 and 1000')
        ],
        render_kw={'id':'start_door_num'}
    )
    error_message = ''
    submit_button = SubmitField('Submit')

    # this doesn't work! why?
    def validate_on_submit(self):
        sv = FlaskForm.validate_on_submit(self)
        if sv:
            if self.doors_num.data < self.loaders_num.data:
                self.error_message = 'The number of loaders cannot exceed the number of doors'
                return False
            if self.loaders_num.data * 4 < self.doors_num.data:
                self.error_message = 'The number of doors cannot exceed four times the number of loaders'
                return False
            
            return True
        
        return False