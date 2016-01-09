# coding: utf-8

import json
from django.db import models

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text.encode('utf-8')

	def toJSON(self):
		voteList = []
		for c in self.choice_set.all():
			voteList.append({'choice_text' : c.choice_text, 'votes' : c.votes})

		return json.dumps({
			'id': self.id,
			'question_text' : self.question_text,
			'pub_date' : self.pub_date.strftime("%Y-%m-%d %H:%M:%S"), # año-mes-dia hora:minutos:segundos
			'votes' : voteList
		})	

class Choice(models.Model):
	question = models.ForeignKey(Question)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text.encode('utf-8')
