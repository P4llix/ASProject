# ASProject

Final project for Web Application subject in my university
Main idea was to create website for gym contest. For entire year contest's administartor is gonna post few exercise for participants. 
Users/participants have to record the exercise performed and send link with video.

## Index route
Database  
![index_db](https://github.com/P4llix/ASProject/blob/main/docs/DB_index.PNG)

Generated preview  
![index](https://github.com/P4llix/ASProject/blob/main/docs/index.png)

## User administration module
### Priviliges
Every page/route that require login is secured in code using python decorators, such as:
/home require just login
```
@app.route('/home')
@login_required
def home():
  ...
```

Decorator ```@login_required``` check if session contain ```auth``` argument
```
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwagrs):
        if session.get('auth', 0) == 1:
            return f(*args, **kwagrs)
        else:
            flash('Potwierdź swoją tożsamość logując się')
            return redirect(url_for('login'))
    return wrap
```


/home/admin/task has additional decorator ```@admin_required``` that by analogy works like ```@login_required``` but check if user has privilage to access this route
```
@app.route('/home/admin/task')
@admin_required
@login_required
def administration_task():
  ...
```

```
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwagrs):
        if 'ADMIN' in user.roles and user.roles['ADMIN'] == 1 :
            return f(*args, **kwagrs)
        else:
            flash('Restricted area')
            return redirect(url_for('home'))
    return wrap
```

### Overview
![user_administration](https://github.com/P4llix/ASProject/blob/main/docs/user_administartion.PNG)

### User detail
![user_administration_detail](https://github.com/P4llix/ASProject/blob/main/docs/user_administartion_detail.PNG)

### User role
![user_administration_role](https://github.com/P4llix/ASProject/blob/main/docs/user_administartion_role.PNG)

## AJAX
To use AJAX first we need to import library in base.html file
```<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>```

Every modal works with AJAX so there is no need to generate separte modal for every single action, just dynamicly load content.
Example below show how AJAX works with python Flask library.
```
$('.show-details').click(function(){
    $.ajax({
        url: '/api/exercise/get',
        type: 'post',
        data: {
            id: $(this).data('exerciseid')
        },
        success: function(data){
            $('#updateIdExercise').val(data[0]);
            $('#updateNazwa').val(data[1]);
            $('#updateOpis').val(data[2]);
            $('#updateLink').val(data[3]);
            $('#modal_exercise_detail').modal('show');
        }
    });
});
```

First we need take data from page using 
```
data: {
    id: $(this).data('exerciseid')
},
```

Next, collected data are send to ```url: '/api/exercise/get'```

```
@app.route('/api/exercise/get', methods = ['POST'])
def api_exercise_get():
    if request.method == 'POST':
        id = request.form['id']

        result = db.exercise_specific(id)
        db.session.commit()

        return jsonify([
            result.ROWID, 
            result.NAME, 
            result.DESCRIPTION, 
            result.LINK
        ])
```
Return sends query result to js part and by using 
```
success: function(data){
    $('#updateIdExercise').val(data[0]);
    $('#updateNazwa').val(data[1]);
    $('#updateOpis').val(data[2]);
    $('#updateLink').val(data[3]);
    $('#modal_exercise_detail').modal('show');
}
```
I can overwerite existing fields with new values


