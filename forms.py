from wtforms import Form, StringField, PasswordField, validators, SubmitField

class LoginForm(Form):
	login = StringField(
		'login', 
		[
			validators.Length(min=1, max=40),
			validators.DataRequired()
		]
	)

	password = PasswordField(
		'password', 
		[
			validators.Length(min=1, max=40), 
			validators.DataRequired()
		]
	)

	submit = SubmitField("Zaloguj")

	new_password = PasswordField(
		'password_new', 
		[
			validators.Length(min=1, max=40), 
			validators.DataRequired(),
		]
	)
	confirm = PasswordField(
		'Powtórz hasło',
		[
			validators.Length(min=1, max=40), 
			validators.DataRequired(),
		]
	)


	submit_new = SubmitField("Zapisz")