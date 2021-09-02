from  flask import Flask,request,render_template
#import render_template for html 

udemy=Flask(__name__)

@udemy.route('/',methods=['GET','POST']) 
def english():
	#return 'hello friend'
	height=0
	weight=0
	ans=0
	if request.method=='POST' and 'height' in request.form:
		height=int(request.form.get('height')) / 100 # or request.form['height']
		weight=int(request.form.get('weight'))
		ans=weight/(height**2)
	return render_template('bmi.html',bmi=ans)

@udemy.route('/german/<string:name>') #is same as @app.route('/',methods=['GET']) flask handles get requests by default
#to get parameters from the url <datatype:varname> is used.
def german(name):
	return 'Holla '+name+' Du bist mein Fruend'

udemy.run(debug=True) #debug=True helps so that we dont have to stop the app in cmd everytime a change has been made
