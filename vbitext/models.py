from django.db import models
from django import forms


class Data(models.Model):
	asso_num = models.CharField(max_length=30)
	asso_input = models.CharField(max_length=500)
	
class term (models.Model):
	name = models.CharField(max_length=50)
	freq = models.CharField(max_length=50)
	
class input (models.Model):
	
	terms=models.ManyToManyField(term)
	
	def freqs (self, term):
		cursor = connection.cursor()
		cursor.execute("""
			SELECT DISTINCT freq
			FROM term_name
			WHERE term == %s""", [term])
			

class Record(models.Model):
	terms = models.ForeignKey(term)