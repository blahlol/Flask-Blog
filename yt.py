from flask import Flask,request,render_template,redirect,abort,jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS #used to allow js to get api data from flask
#import render_template for html 


yt=Flask(__name__)
yt.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqldb.db'
db=SQLAlchemy(yt)
CORS(yt)
 
class blogpost(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	author=db.Column(db.String(20),nullable=False)
	content=db.Column(db.Text,nullable=False)

	def __repr__(self):
		return 'blogpost' + str(self.id) #prints when we use query.all()

@yt.route('/')
def home():
	#return abort(404)
	return render_template('home.html')
	
#posts=[{'author':'Walt','content':'Say my Name'},{'author':'Jesse','content':'Yeah! Science!'}] #assume this to be sample db
@yt.route('/posts') 
def posts():   #method name isnt used anywhere like action or redirection so it can be anything. only route values are used.
	all_posts=blogpost.query.all()   #blogpost.query.order_by(blogpost.author).all() order_by is used for sorting.
	return render_template('index.html',value=all_posts)

@yt.route('/newpost',methods=['GET','POST'])
def newpost():
	if request.method=='POST':
		newcontent=request.form['content']
		newauthor=request.form['author']
		new_post=blogpost(content=newcontent,author=newauthor)
		db.session.add(new_post)
		db.session.commit()
		return redirect('/posts') #route values
	else:
		return render_template('newpost.html')

@yt.route('/posts/delete/<int:id>')
def delete(id):
	db.session.delete(blogpost.query.get_or_404(id))
	db.session.commit()
	return redirect('/posts')

@yt.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
	post=blogpost.query.get_or_404(id)
	if request.method=='POST':
		content=request.form['content']
		author=request.form['author']
		post.author=author
		post.content=content
		db.session.commit()
		return redirect('/posts')
	else:
		return render_template('edit.html',post=post) 

@yt.route('/api')
def api():
	posts=[{'author':'Walt','content':'Say my Name'},{'author':'Jesse','content':'Yeah! Science!'}]
	return jsonify(posts)


#this would execute if some page is not found (error 404) so 404 is passed as arg to the error handler. 
#to execute this function include a abort(404)  statement in places where there is a chance that something might go wrong and pages might not be found.
@yt.errorhandler(404)
def error(error):
	return render_template('not_found.html') , 404

if __name__=='__main__':
	yt.run(debug=True) #debug=True helps so that we dont have to stop the app in cmd everytime a change has been made
