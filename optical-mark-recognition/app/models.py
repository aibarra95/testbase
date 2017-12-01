from app import db

class Student(db.Model):
	studentId = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String(64), index=True)
	lastName = db.Column(db.String(64), index=True)
	graded = db.relationship('GradedTest', backref='student', lazy='dynamic')

	def __repr__(self):
		return '<Student %r>' % (self.firstName)

class Test(db.Model):
	testId = db.Column(db.Integer, primary_key=True)
	testName = db.Column(db.String(64), index=True)
	numberOfQuestions = db.Column(db.Integer, index=True)
	testAverage = db.Column(db.Integer, index=True)
	gradedTest = db.relationship('GradedTest', backref='test', lazy='dynamic')
	
	def __repr__(self):
		return '<Test %r>' % (self.testName)

class GradedTest(db.Model):
	gradedId = db.Column(db.Integer, primary_key = True)
	testId = db.Column(db.Integer, db.ForeignKey('test.testId'))
	studentId = db.Column(db.Integer, db.ForeignKey('student.studentId'))
	correct = db.Column(db.Integer, index=True)

	def __repr__(self):
		return '<Graded Test %r>' % (self.gradedTestId)
