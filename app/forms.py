from wtforms import Form, StringField, validators, BooleanField, PasswordField, ValidationError

from app.models import Task


class TaskForm(Form):

    title = StringField('Title', [validators.Length(min=4, max=25, message='Title 4 to 25 characters'), validators.DataRequired()])
    description = StringField('Description', [validators.Length(max=500), validators.DataRequired()])
    done = BooleanField('Done', [validators.DataRequired()])

    # def __init__(self, *args, **kwargs):
    #     # self.title = kwargs.get('title', None)
    #     # self.description = kwargs.get('description', None)
    #     # self.done = kwargs.get('done', None)
    #     super(TaskForm, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'Title: {}, Description: {}, Done: {}'.format(self.title, self.description, self.done)

    # @staticmethod
    # def populate(data):
    #     pass

    def save(self):
        pass

    def get_task(self):
        return Task(title=self.title.data, description=self.description.data)


# http://wtforms.readthedocs.io/en/latest/validators.html
# http://werkzeug.pocoo.org/docs/0.12/routing/#rule-format
class Length(object):
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        if not message:
            message = u'Field must be between %i and %i characters long.' % (min, max)
        self.message = message

    def __call__(self, form, field):
        l = field.data and len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            raise ValidationError(self.message)


length = Length


class RegistrationForm(Form):
    username = StringField('Username', [
        length(min=4, max=25),
        validators.Regexp('^\w+$', message='Username must contain only letters numbers or underscore')
    ])
    email = StringField('Email Address', [
        validators.DataRequired('Please enter email address'),
        validators.Length(min=6, max=35), validators.Email(message='Please enter valid email address')
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    education = StringField('Education', [
        validators.Optional(),
        validators.AnyOf(['B-Tech', 'Graduate', 'Post Graduate'], message='Can only be B-Tech, Graduate, Post Graduate')])
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        # Form.__init__(self, *args, **kwargs)
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.creator = None

    def validate(self):
        rv = super(RegistrationForm, self).validate()
        if not rv:
            return False

        self.creator = 'Some object reference'
        return True


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        # user = User.query.filter_by(
        #     username=self.username.data).first()
        # if user is None:
        #     self.username.errors.append('Unknown username')
        #     return False
        #
        # if not user.check_password(self.password.data):
        #     self.password.errors.append('Invalid password')
        #     return False

        user = None
        if self.username.data == 'john' and self.password.data == 'john':
            user = {'user': self.username.data}
        else:
            self.username.errors.append('Invalid username or password')
            return False
        self.user = user

        return True
