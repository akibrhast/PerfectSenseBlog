from flask import request
from flask_wtf import FlaskForm,Form
from wtforms import StringField, SubmitField, TextAreaField,SelectMultipleField,BooleanField,Field,HiddenField
from wtforms.validators import ValidationError, DataRequired, Length,Regexp
from flask_babel import _, lazy_gettext as _l
from app.models import User
from markupsafe import Markup



from wtforms.widgets.core import HTMLString, html_params, escape

class RichTextFieldWidget(object):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)        # Allow passing title= or alternately use field.description

        html = "<div %s>  </div>"
        return HTMLString(html % html_params(class_='editor',id='editor'))


class RichTextField(Field):
    widget = RichTextFieldWidget()
 
class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

class SelectTag(FlaskForm):
    search = SubmitField("Search Tag")

class DeleteTag(FlaskForm):
    delete = SubmitField("Delete Tag")

class TagList(SelectTag, DeleteTag):
    tags = SelectMultipleField('Tag', choices=[], coerce=int,)

class TagWithAdd(FlaskForm):
    tags = SelectMultipleField('Tag', choices=[], coerce=int)

class AddTag(FlaskForm):
    name = StringField('TagName', validators=[DataRequired(), Regexp('^[A-Za-z]+$')])
    submit = SubmitField('Add Tag')


class PostForm(TagWithAdd):
    hiddenField = HiddenField(id='rtfhidden',validators=[DataRequired()])
    title = StringField('Title')
    post = RichTextField()
    submit = SubmitField(_l('Submit'))

class CommentForm(FlaskForm):
    comment = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

