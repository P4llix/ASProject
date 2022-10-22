from wtforms import Form, StringField, PasswordField, validators, SubmitField

class LoginForm(Form):
	username = StringField(
		'Username' ,[
			validators.Length(min=1, max=40),
			validators.DataRequired()
			]
		)

	password = PasswordField(
		'Email Address', [
		validators.Length(min=1, max=40), 
		validators.DataRequired()
			]
		)

	submit = SubmitField("Zaloguj")