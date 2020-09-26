from flask import Flask, request, Blueprint, render_template, redirect, session, url_for
from ..models import Task
from ..core import login_required

# create a blueprint
bp = Blueprint('task', __name__)

@bp.route('/task/create/<string:tasklist_id>', methods=['GET', 'POST'])
@login_required
def create_task(tasklist_id):
    if request.method == 'GET':
        # render the create task template
        return render_template('task/create.html')
    else:
        # read values from the form submit
        title = request.form['task-title']
        description = request.form['task-description']

        # create a task document
        task = Task(title = title, description = description, tasklist_id = tasklist_id)


        # save the tasklist document
        task.save()
        print(title,description)
        
        # redirect to the index
        return redirect(url_for('tasklists.view_tasklist', tasklist_id = tasklist_id))

@bp.route('/task/<string:tasklist_id>/<string:task_id>')
@login_required
def view_task(tasklist_id,task_id):
  
    task = Task.query.get_or_404(task_id)
    
    return render_template('tasks/view-task.html', task = task)
    
@bp.route('/task/update/<tasklist_id>/<string:task_id>',methods=['GET','POST'])
@login_required
def update_task(tasklist_id,task_id):

    task = Task.query.get_or_404(task_id)

    # if the tasklist was found
    if task:
        
        if request.method == 'GET':
            # render the update list form with pre-populated values
            return render_template('tasks/update-task.html',task=task )
        else:

            # read the values from the update list form
            title = request.form['task-title']
            description = request.form['task-description']

            task.title= title
            task.description = description

            task.save()
           
            # redirect to the 'view_list' view
            return render_template('index.html', tasklist_id = tasklist_id,task_id=task_id)

@bp.route('/task/delete/<string:tasklist_id>/<string:task_id>', methods=['GET'])
@login_required
def delete_task(tasklist_id, task_id):
    task = Task.query.get_or_404(task_id)
    task.remove()

    # redirect to the index
    return redirect(url_for('tasklists.view_tasklist', tasklist_id = tasklist_id))

