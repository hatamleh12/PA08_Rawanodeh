from flask import Flask, request, Blueprint, render_template, redirect, session, url_for
from ..models import TaskList, Task, User
from ..core import login_required

# create a blueprint
bp = Blueprint('tasklists', __name__)


@bp.route('/tasklist/create', methods=['GET', 'POST'])
@login_required
def create_tasklist():
    if request.method == 'GET':
        # render the create tasklist template
        return render_template('tasklist/create.html')
    else:
        # read values from the form submit
        name = request.form['list-name']
        description = request.form['list-description']

        # create a tasklist document
        tasklist = TaskList(name = name, description = description, owner_id = session['user']['id'])

        # save the tasklist document
        tasklist.save()

        # get the logged in user
        user = User.query.get_or_404(session['user']['id'])

        # add the newly created tasklist
        user.add_tasklist(str(tasklist.mongo_id))

        # save the changes to the user object
        user.save()

        # update the session
        session['user'] = user.serialized

        # redirect to the index
        return redirect(url_for('tasklists.tasklists'))


@bp.route('/tasklist/<string:tasklist_id>')
@login_required
def view_tasklist(tasklist_id):
    tasklist = TaskList.query.get_or_404(tasklist_id)
    tasks = Task.query.filter(Task.tasklist_id == tasklist_id).all()
    return render_template('tasklist/view.html', tasklist = tasklist, tasks = tasks)

@bp.route('/tasklist/update/<tasklist_id>',methods=['GET','POST'])
@login_required
def update_tasklist(tasklist_id):

    tasklist = TaskList.query.get_or_404(tasklist_id)

    # if the tasklist was found
    if tasklist:
        
        if request.method == 'GET':
            # render the update list form with pre-populated values
            return render_template('tasklist/update-list.html',tasklist=tasklist )
        else:

            # read the values from the update list form
            name = request.form['list-name']
            description = request.form['list-description']

            tasklist.name = name
            tasklist.description = description

            tasklist.save()
           
            # redirect to the 'view_list' view
            return redirect(url_for('tasklists.view_tasklist', tasklist_id=tasklist_id))
    
@bp.route('/tasklist/delete/<string:tasklist_id>')
@login_required
def delete_tasklist(tasklist_id):
    # retrieve the tasklist
    tasklist = TaskList.query.get_or_404(tasklist_id)
    
    # delete the tasklist
    tasklist.remove()
    
    # redirect the user to the tasklists
    return redirect(url_for('tasklists.tasklists'))


@bp.route('/tasklists')
@login_required
def tasklists():   
    # create a list to store the tasklists
    tasklists = TaskList.query.filter(TaskList.owner_id == session['user']['id'])

    
    # render the task lists template
    return render_template('tasklist/task-lists.html', tasklists = tasklists)

@bp.route('/search', methods=['GET','POST'])
def search():
    if request.method=='GET':
        return render_template('search/search.html')
    else:    

        search_keyword = request.form['search-keyword']

        # search_results = Task.query.filter(Task.title.like('%' + search_keyword+ '%')).all()
        search_results = Task.query.filter(
            {
                '$or': [
                    {Task.title: {"$regex": search_keyword}},
                    {Task.description: {"$regex": search_keyword}}
                ]       
            }
            ).all()

        print(search_results,search_keyword)
          
        return render_template('search/results.html',results=search_results,keyword=search_keyword)

@bp.route('/favorites' ,methods=['GET'])
def view_favorites():

    if request.method=='GET':
        favorites_tasklists = TaskList.query.filter(
            {
                '$and': [
                    {TaskList.owner_id:session['user']['id'] },
                    {TaskList.is_favorite:True}
                ]       
            }
            ).all()


        return render_template('tasklist/favorites.html',tasklists=favorites_tasklists)

@bp.route('/private' ,methods=['GET'])
def view_private():

    if request.method=='GET':
        private_tasklists = TaskList.query.filter(
            {
                '$and': [
                    {TaskList.owner_id:session['user']['id'] },
                    {TaskList.is_private:True}
                ]       
            }
            ).all()


        return render_template('tasklist/private.html',tasklists=private_tasklists)



@bp.route('/favorite/<tasklist_id>')    
def set_favorite(tasklist_id):
    
    tasklist =TaskList.query.get_or_404(tasklist_id)

    if tasklist.is_favorite == True:

        tasklist.is_favorite = False
    else:
        tasklist.is_favorite = True

    tasklist.save()
    return redirect('/favorites')  

@bp.route('/tasklist/private/<tasklist_id>',methods=['GET','POST'])    
def mark_private(tasklist_id):

    tasklist =TaskList.query.get_or_404(tasklist_id)

    if tasklist.is_private == True :

        tasklist.is_private = False
    else:

        tasklist.is_private = True

    tasklist.save()

    return redirect('/private')   

@bp.route('/overdue/tasklist/<tasklist_id>', methods =['GET'])
@login_required
def view_overdue(tasklist_id  ):
    tasklists = TaskList.query.filter(TaskList.owner_id == session['user']['id'])
    # if request.method == 'GET':
    #     return render_template('tasklist/overdue.html',tasklists=tasklists)
    print(tasklists)
            
    return render_template('index.html', tasklists =tasklists , tasklist_id =tasklist_id )

    


 