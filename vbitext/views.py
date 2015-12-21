# Create your views here
from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from models import Data
from stat import *
import re




import threading
import multiprocessing


class myThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print "Starting " + self.name+"\r\n"
        create_file(self.name)
        print "Exiting " + self.name


def worker(num2, threadList):
	newlist=[]
	num = len(threadList)/4
	print "Worker:", num2
	if len(threadList)<4:
		newlist=threadList
		
	else:
		if num2==1:
			newlist=threadList[0:num]
		elif num2==2:
			newlist=threadList[num:num*2]
		elif num2==3:
			newlist=threadList[num*2:num*3]
		elif num2==4:
			newlist=threadList[num*3:-1]
	# Create new threads
	threads=[]
	for tName in newlist:
		thread = myThread(tName)
		thread.start()
		threads.append(thread)

	# Wait for all threads to complete
	
	for t in threads:
		t.join()
	print "Exiting Main Thread"
	return



def about (request):
	return render (request, 'about.html')

def analyze_form (request):
	return render (request, 'search_form.html')

def analyze(request):
	
	if 'genes' in request.GET and request.GET['genes']:
		genes = request.GET['genes']
		genes1=set()
		if '\r\n' in genes:
			genes=genes.split('\r\n')
			for gene in genes:
				gene=gene.strip()
				if ',' in gene:
					gene=gene.split(', ')
				else:
					gene=[gene]
				genes1.update(gene)
		elif ',' in genes:
			genes=genes.split(', ')
			for gene in genes:
				gene=gene.strip()
				gene=[gene]
				genes1.update(gene)
		else:
			genes1=[genes]

			
		genes1=list(genes1)
			
		counts=len(genes1)

		# Create new threads
		threads=[]
		for tName in genes1:
			thread = myThread(tName)
			thread.start()
			threads.append(thread)

		# Wait for all threads to complete
		
		for t in threads:
			t.join()
		print "Exiting Main Thread"
	
		genes_new=[]
		final,numabs,descrip=create_data(genes1)
		final1=[]
		for item in final:
			final1.append(item[0:100])
		unknown=0
		for gene in genes1:	
			if os.path.isfile(''+gene.upper()+".txt"):
				genes_new.append(gene)
			else:
				genes_new.append('<font color="red">'+gene+'</font>')
				unknown+=1
		ratio=counts-unknown
		return render (request, 'analyze_data.html',
			{'genes_new':genes_new, 'seed':1000,'unknown':unknown, 'final':final1,
			'count':counts, 'genes':genes1, 'numabs':numabs, 'ratio':ratio, 'descrip':descrip})
	else:
		return render (request, 'search_form.html', {'error': True})

def reanalyze(request):
	term=[]
	if 'abstract' in request.GET:
		return disp_abs(request)
	elif 'resubmit' in request.GET:
		if 'item' in request.GET and request.GET['item']:
			item = request.GET.getlist('item')
			if len(item)< 1:
				return render (request, 'search_form.html', {'error': True})
			list=[]
			for term in item:
				term=term.replace(",",'')
				term=term.replace("(",'')
				term=term.replace("'",'')
				list.append(term)
		
			# Create new threads
			threads=[]
			for tName in list:
				thread = myThread(tName)
				thread.start()
				threads.append(thread)

			# Wait for all threads to complete
			
			for t in threads:
				t.join()
			print "Exiting Main Thread"
			
			counts=len(list)

			final,numabs,descrip=create_data(list)
			final1=[]
			for item in final:
				final1.append(item[0:100])
			genes_new=[]
			unknown=0
			for gene in list:
				if os.path.isfile(''+gene.upper()+".txt"):
					genes_new.append(gene)
			else:
				genes_new.append('<font color="red">'+gene+'</font>')
				unknown+=1
			ratio = counts-unknown		
			return render (request, 'analyze_data.html',
				{'genes_new':genes_new, 'genes':list,'unknown':unknown,
				'seed':1000, 'count':counts, 'numabs':numabs, 'ratio':ratio, 'descrip':descrip,
				'final':final1})
		else:
			return render (request, 'search_form.html', {'error': True})
			
	elif 're2' in request.GET:
		if 'item' in request.GET:
			list = request.GET.getlist('item')
		else:
			return render (request, 'search_form.html', {'error': True})
		genes = request.GET['genes']	
		genes=genes.split(', ')
		
		# Create new threads
		threads=[]
		for tName in list:
			thread = myThread(tName)
			thread.start()
			threads.append(thread)

		# Wait for all threads to complete
		
		for t in threads:
			t.join()
		print "Exiting Main Thread"
		
		
		final,numabs,descrip=create_data(list+genes)
		final1=[]
		for item in final:
			final1.append(item[0:100])
		both = list+genes
		genes_new=[]
		unknown=0
		for gene in both:
			if os.path.isfile(''+gene.upper()+".txt"):
				genes_new.append(gene)
			else:
				genes_new.append('<font color="red">'+gene+'</font>')
				unknown+=1
		counts=len(list+genes)
		ratio = counts-unknown
		return render (request, 'analyze_data.html',
				{'genes':list+genes, 'genes_new':genes_new, 'unknown':unknown,
				'seed':1000, 'count':counts, 'numabs':numabs, 'ratio':ratio, 'descrip':descrip,
				'final':final1})
		

	
	elif 'search' in request.GET:
		search = request.GET['search']
		search=search.split(', ')
		searched=[]
		genes = request.GET['genes']
		genes=genes.split(', ')
		print 'Creating the list'
		final,numabs,descrip=create_data(genes)
		final1=[]
		for item in final:
			final1.append(item[0:100])
		genes_new=[]
		unknown=0
		for gene in genes:
			if os.path.isfile(''+gene.upper()+".txt"):
				genes_new.append(gene)
			else:
				genes_new.append('<font color="red">'+gene+'</font>')
				unknown+=1
			
		counts=len(genes)
		ratio = counts-unknown
		print 'Searching the list'
		for i in search:
			for entry in final[0]:
				if entry[0].lower()==i.lower():
					print 'Appended to query'
					searched.append(entry)
					break
				else:
					pass
			for entry in final[1]:
				if entry[0].lower()==i.lower():
					print 'Appended to query'
					searched.append(entry)
					break
				else:
					pass
			for entry in final[2]:
				if entry[0].lower()==i.lower():
					print 'Appended to query'
					searched.append(entry)
					break
				else:
					pass
		return render (request, 'analyze_data.html',
		{'genes':genes, 'genes_new':genes_new,'unknown':unknown, 'seed':1000, 'count':counts,
		 'val':searched, 'numabs':numabs, 'ratio':ratio, 'descrip':descrip, 'final':final1})
		
def query (request):
	return render(request, 'GeneText2.html')
	
def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))
	
from Bio import Entrez, Medline
import operator
from os import path
from operator import itemgetter
import urllib2
import httplib
import re
import os
Entrez.email ="nathir2@vbi.vt.edu"

def create_file (gene):
	bad_word_key={}
	count3=0
		
	with open('bad_word_key.txt') as data:
		contents = (line.rstrip('\r\n') for line in data)
		for line in contents:
			if line:
				line=line.rstrip()
				bad_word_key[line]=1
		
	bad_word_key[gene]=1
	gene=gene.upper()
	gene=gene.strip()
	if os.path.isfile(gene+".txt"):
		print "file found for %s" %gene
	
		return
	
	
	try:		
		search_results = Entrez.read(Entrez.esearch(db="pubmed",
								term=gene, reldate=72000, date="pdat",
								usehistory="y"))
	except (RuntimeError,urllib2.HTTPError):
		pass
	
	print "Creating a file for %s . . ."% gene
	count = int(search_results["Count"])
	
	if count==0:
		pass
		
	
	batch_size = 10000
	count2=min(count,20000)
	all_dict={}
	abstracts=[]
	mesh_dict={}

	for start in range(0,count2,batch_size):
		records=[]
		try:
			end = min(count2, start+batch_size)
			handle = Entrez.efetch(db="pubmed",
							rettype="medline", retmode="text",
							retstart=start, retmax=batch_size,
							webenv=search_results["WebEnv"],
							query_key=search_results["QueryKey"])
			records=Medline.parse(handle)
		except (KeyError, urllib2.HTTPError, httplib.IncompleteRead):
			continue	
		
		print "Separating Abstract . . ."
		
		
		for record in records:
			
			try:
				abstract=record['AB']
				mesh = record['OT']
			except (KeyError, httplib.IncompleteRead) :
				continue
	
			abstract=abstract.translate(None, """?.!;:\,>"<'[]{}()@#$%^&*|""")
			
			
			for m in mesh:
				if m in mesh_dict:
					mesh_dict[m]+=1
				else:
					mesh_dict[m]=1
			
			
			abstract=[ element for element in abstract.split() if element not in bad_word_key and len(element)>2]
			
			
			
			for k in range(0,len(abstract)):
				
				try:
					all_dict[abstract[k]]+=1
				except KeyError:
					all_dict[abstract[k]]=1
				
					
				if k < len(abstract)-1:	
					try:
						all_dict[abstract[k]+" "+abstract[k+1]]+=1
					except KeyError:
						all_dict[abstract[k]+" "+abstract[k+1]]=1
				else:
					pass
				
				
				if k < len(abstract)-2:
					try:
						all_dict[abstract[k]+" "+abstract[k+1]+" "+abstract[k+2]]+=1
					except KeyError:
						all_dict[abstract[k]+" "+abstract[k+1]+" "+abstract[k+2]]=1
				else:
					pass
				
					
				if k < len(abstract)-3:
					try:
						all_dict[abstract[k]+" "+abstract[k+1]+" "+abstract[k+2]+" "+abstract[k+3]]+=1
					except KeyError:
						all_dict[abstract[k]+" "+abstract[k+1]+" "+abstract[k+2]+" "+abstract[k+3]]=1
				else:
					pass
	

	if len(all_dict)==0:
		return
		
	print "Slicing and dicing data"
	all_dict=sorted(all_dict.iteritems(), key= operator.itemgetter(1), reverse=True)
	var = min(len(all_dict),200000)
	
	mesh_dict=sorted(mesh_dict.iteritems(), key= operator.itemgetter(1), reverse=True)
	
	try:
		del bad_word_key[gene]
	except KeyError:
		pass
		
	with open(gene+'.txt',"w") as f:
		print >>f, str(min(count,20000))+'\r\n'
		for j in range(0,var):
			print >>f, gene+',', all_dict[j][0]+",", str(all_dict[j][1])+'\r\n'
	
	with open(gene+'_mesh.txt','w') as f2:
		for y in range(0, len(mesh_dict)):
			print >>f2, gene+'|', mesh_dict[y][0]+'|', str(mesh_dict[y][1])+'\r\n'			


			
def create_data(genes, seed=1000):
	all_dict={}
	unique_dict={}
	unique_net={}
	unique_genesdict={}
	unique_genesnet={}
	genes_dict={}
	genes_list={}
	bad_word_key={}
	count=0
	reference_key={}
	final_dict={}
	disease_dict={}
	disease_list={}
	unique_diseasedict={}
	unique_diseasenet={}
	mesh_dict={}
	unique_meshdict={}
	unique_meshnet={}
	numabs=0
	descrip=[]
	disin=[]
	notin=[]
	
	with open('reference_key.txt') as data:
		reference = (line.rstrip('\r\n') for line in data)
		for line in reference:
			if line:
				line=line.split(', ')
				reference_key[line[0]]=int(line[1])	
		
			
	with open('disease_list.txt') as f5:
		diseases = (line.rstrip('\r\n') for line in f5)
		for line in diseases:
			disease_dict[line.lower()]=1
	
	with open('genedb.txt') as f6:
		genedb = (line.rstrip('\r\n') for line in f6)
		for line in genedb:
			try:
				line=line.split(', ')
				genes_dict[line[0]]=line[1]
			except IndexError:
				continue
	
	
			
	for gene in genes:
	
		try:
			with open(gene+".txt"): pass
		except IOError:
			continue
			
		num=0
		num2=0
		retMax='-'
		unique_list=[]
		unique_disease=[]
		unique_gene=[]
		unique_genes=[]
		unique_mesh=[]
		gene1=''
		gene1=gene
		gene=gene.upper()
		gene=gene.strip()
		head=[]
		with open (gene+'.txt') as f:
			head = [f.next() for x in xrange(1)]
			numabs+=int(head[0].rstrip('\r\n'))
			contents=(line.rstrip('\r\n') for line in f)
			for line in contents:
				if line:
					line = line.split(', ')
					
					try:
												
						if line[1].lower() in disease_dict:
							unique_disease.append([line[0],line[1],line[2]])
							if line[1].lower() in disease_list:
								disease_list[line[1].lower()]+=int(line[2])
							else:
								disease_list[line[1].lower()]=int(line[2])
								

						
						elif line[1] in genes_dict:
							unique_genes.append([line[0],line[1],line[2]])
							if line[1] in genes_list:
								genes_list[line[1]]+=int(line[2])
							else:
								genes_list[line[1]]=int(line[2])
						
						else:
							unique_list.append([line[0],line[1],line[2]])
							if line[1] in all_dict:
								all_dict[line[1]]+=int(line[2])	
							else:
								all_dict[line[1]]=int(line[2])
							
										
						#r = re.compile("[A-Z][a-z]{2}[A-Z][0-9]{*}[A-Z]{*}[0-9]{*}")
						#r2 = re.compile("[A-Z][A-Z][A-Z][A-Z][0-9]")
						
						# if r2.match(line[1]):
							# unique_genes.append(line[1])
							# if line[1] in genes_list:
								# genes_list[line[1]]+=int(line[2])
							# else:
								# genes_list[line[1]]=int(line[2])
								
						
							
					except IndexError:
						pass
						
					
						
		with open(gene+'_mesh.txt') as data2:
			contents=(line2.rstrip('\r\n') for line2 in data2)
			for line2 in contents:
				if line2:
					line2 = line2.split('| ')
					try:
						if line2[1] in mesh_dict:
							mesh_dict[line2[1]]+=int(line2[2])
						else:
							mesh_dict[line2[1]]=int(line2[2])
						unique_mesh.append([line2[0],line2[1]])
					except IndexError:
						pass
					
		for mesh in unique_mesh:
			if mesh[1] in unique_meshdict:
				unique_meshdict[mesh[1]]+=1
				unique_meshnet[mesh[1]]+=(mesh[0],)
			else:
				unique_meshdict[mesh[1]]=1
				unique_meshnet[mesh[1]]=(mesh[0],)
		
		for word in unique_list:
			if word[1] in unique_dict:
				unique_dict[word[1]]+=1
				unique_net[word[1]]+=(word[0],)
			else:
				unique_dict[word[1]]=1
				unique_net[word[1]]=(word[0],)
				
		for word in unique_genes:
			if word[1] in unique_genesdict:
				unique_genesdict[word[1]]+=1
				unique_genesnet[word[1]]+=(word[0],)
			else:
				unique_genesdict[word[1]]=1
				unique_genesnet[word[1]]=(word[0],)
				
		
		for word in unique_disease:
			if word[1].lower() in unique_diseasedict:
				if word[0] in unique_diseasenet[word[1].lower()]:
					continue
				else:
					unique_diseasedict[word[1].lower()]+=1
					unique_diseasenet[word[1].lower()]+=(word[0],)
			else:
				unique_diseasedict[word[1].lower()]=1
				unique_diseasenet[word[1].lower()]=(word[0],)
		
		
		if gene1.lower() in disease_dict:
			try:
				handler = Entrez.egquery(term=gene1)
				recorder = Entrez.read(handler)
				for row in recorder["eGQueryResult"]:
					if row["DbName"]=="pubmed":
						retMax = row["Count"]
			except RuntimeError:
				pass
			
			
			with open(''+gene+'.txt','r') as data4:
						try:
							seem = [data4.next() for x in xrange(200)]
						except StopIteration:
							pass
						seem=seem[3:200]
						seem1=''
						seem2=''
						for item in seem:
							item=item.rstrip('\r\n')
							item=item.rstrip('\n')
							item=item.split(', ')
							if len(item)==3:
								if item[1] in disease_dict:
									seem1+=item[1]+', '
								elif item[1] in genes_dict:
									seem2+=item[1]+', '
						
			
			descrip.append([gene1,'disease',retMax,'','','', seem1, seem2])	
			
		elif gene1 in genes_dict:
			try:
				handler = Entrez.egquery(term=gene1)
				recorder = Entrez.read(handler)
				for row in recorder["eGQueryResult"]:
					if row["DbName"]=="pubmed":
						retMax = row["Count"]
			except (RuntimeError, urllib2.HTTPError):
				pass
			
					
			with open(''+gene+'.txt','r') as data4:
						try:
							seem = [data4.next() for x in xrange(200)]
						except StopIteration:
							pass
						seem=seem[3:200]
						seem1=''
						seem2=''
						for item in seem:
							item=item.rstrip('\r\n')
							item=item.rstrip('\n')
							item=item.split(', ')
							if len(item)==3:
								if item[1] in disease_dict:
									seem1+=item[1]+', '
								elif item[1] in genes_dict:
									seem2+=item[1]+', '
			annotations=[]
			try:
				handle = Entrez.esearch(db="gene",term=gene1, retmax=100)
				record = Entrez.read(handle)
				id_list = record["IdList"]
				request = Entrez.epost("gene",id=",".join(id_list))
				result = Entrez.read(request)
				webEnv = result["WebEnv"]
				queryKey = result["QueryKey"]
				data = Entrez.esummary(db="gene", webenv=webEnv, query_key =queryKey)
				annotations = Entrez.read(data)
			except (urllib2.HTTPError, RuntimeError, httplib.IncompleteRead):
				pass
				
			
			alias=''
			gene_name=''
			for gene_data in annotations:
				if gene_data["NomenclatureSymbol"]==gene1:
					alias = gene_data["OtherAliases"]
					org_name = gene_data["Orgname"]
					gene_name = gene_data["Description"]
					descrip.append([gene1,'gene',retMax,gene_name,org_name,alias, seem1,seem2])
					break
				elif gene1 in gene_data["OtherAliases"].split(', '):
					org_name=gene_data['Orgname']
					alias = gene_data["OtherAliases"]
					gene_name = gene_data["Description"]
					gene_new=gene_data["NomenclatureSymbol"]
					descrip.append([gene1 +' OR ' +gene_new,'gene',retMax,gene_name,org_name,alias, seem1, seem2])
					break
				elif gene_data["Name"]==gene1:
					alias = gene_data["OtherAliases"]
					org_name = gene_data["Orgname"]
					gene_name = gene_data["Description"]
					descrip.append([gene1,'gene',retMax,gene_name,org_name,alias, seem1,seem2])
					break
#			unique_genesdict1 = sorted(unique_genesdict.iteritems(), key=operator.itemgetter(1), reverse=True)
			
			

		else:
			try:
				handler = Entrez.egquery(term=gene1)
				recorder = Entrez.read(handler)
				for row in recorder["eGQueryResult"]:
					if row["DbName"]=="pubmed":
						retMax = row["Count"]
			except RuntimeError:
				pass
			
			
			try:
				handle = Entrez.esearch(db="gene",term=gene1, retmax=100)
			except urllib2.HTTPError:
				pass
				
			record = Entrez.read(handle)
			id_list = record["IdList"]
			request = Entrez.epost("gene",id=",".join(id_list))
			annotations=[]
			try:
				result = Entrez.read(request)
				webEnv = result["WebEnv"]
				queryKey = result["QueryKey"]
				data = Entrez.esummary(db="gene", webenv=webEnv, query_key =queryKey)
				annotations = Entrez.read(data)
			except RuntimeError:
				pass
			alias=''
			gene_name=''
			for gene_data in annotations:
				if gene_data["NomenclatureSymbol"]==gene1:
					org_name=gene_data['Orgname']
					alias = gene_data["OtherAliases"]
					gene_name = gene_data["Description"]
					descrip.append([gene1,'gene',retMax,gene_name,org_name,alias])
					with open('genedb.txt','a') as file:
						file.write('\r\n'+gene1+', 1')
					break
				elif gene1 in gene_data["OtherAliases"].split(', '):
					org_name=gene_data['Orgname']
					alias = gene_data["OtherAliases"]
					gene_name = gene_data["Description"]
					gene_new=gene_data["NomenclatureSymbol"]
					descrip.append([gene1 +' OR ' +gene_new,'gene',retMax,gene_name,org_name,alias])
					#genes.append(gene_new)
					with open('genedb.txt','a') as file:
						file.write(gene1+', 1')
					break
				elif gene_data["Name"]==gene1:
					org_name=gene_data['Orgname']
					alias = gene_data["OtherAliases"]
					gene_name = gene_data["Description"]
					descrip.append([gene1,'gene',retMax,gene_name,org_name,alias])
					with open('genedb.txt','a') as file:
						file.write('\r\n'+gene1+', 1')
					break
				elif retMax > 20:
					with open(gene+'.txt','r') as data4:
						seem = [data4.next() for x in xrange(10)]
						seem=seem[1:10]
						for item in seem:
							item=item.translate(None,',').rstrip('\r\n')
							if 'disease' in item:
								with open('disease_list.txt','a') as file:
									file.write('\r\n'+gene1)
								descrip.append([gene1,'disease',retMax,seem[0:5]])
								break
							if 'treatment' in item:
								with open('treatmentdb.txt','a') as file:
									file.write('\r\n'+gene1)
								descrip.append([gene1,'treatment',retMax])
								break
							if 'therapy' in item or 'therapies' in item:
								with open('treatmentdb.txt','a') as file:
									file.write('\r\n'+gene1)
								descrip.append([gene1,'therapy',retMax])
								break
							if 'gene' in item:
								descrip.append([gene1,'gene',retMax])
								break
						break						
							
				else:
					descrip.append([gene1,'test','Number of Abstracts: '+ retMax])
					break
			
		
		
	for q in all_dict:
		if q in reference_key:
			
			exp_freq = (reference_key[q])
			act_freq= all_dict[q]
			freq=0
			if exp_freq> 0:
				final_dict[q]=act_freq*10/exp_freq
			else:
				final_dict[q]=act_freq/1000
			
		else:
			final_dict[q]=all_dict[q]/100

	unique_dict=sorted(unique_dict.iteritems(),key=operator.itemgetter(0))
	all_dict=sorted(all_dict.iteritems(), key= operator.itemgetter(0))
	unique_net=sorted(unique_net.iteritems(),key=operator.itemgetter(0))
	for m in range(0,len(all_dict)):
		all_dict[m]+=(unique_dict[m][1],)
		all_dict[m]+=(unique_net[m][1],)
		all_dict[m]+=(final_dict[all_dict[m][0]],)
	all_dict.sort(key = operator.itemgetter(4), reverse=True)
	

	
	
	genes_list = sorted(genes_list.iteritems(), key=operator.itemgetter(0), reverse=True)
	unique_genesdict = sorted(unique_genesdict.iteritems(), key=operator.itemgetter(0), reverse=True)
	unique_genesnet = sorted(unique_genesnet.iteritems(), key=operator.itemgetter(0), reverse=True)
	for p in range(0,len(genes_list)):
		genes_list[p]+=(unique_genesdict[p][1],)
		genes_list[p]+=(unique_genesnet[p][1],)
	genes_list.sort(key = operator.itemgetter(2,1), reverse=True)
	

	disease_list = sorted(disease_list.iteritems(), key=operator.itemgetter(0), reverse=True)
	unique_diseasedict = sorted(unique_diseasedict.iteritems(), key=operator.itemgetter(0), reverse=True)
	unique_diseasenet= sorted(unique_diseasenet.iteritems(), key=operator.itemgetter(0), reverse=True)
	for y in range(0,len(disease_list)):
		disease_list[y]+=(unique_diseasedict[y][1],)
		disease_list[y]+=(unique_diseasenet[y][1],)
	disease_list.sort(key = operator.itemgetter(2,1), reverse=True)
	
	
	mesh_dict = sorted(mesh_dict.iteritems(),key=operator.itemgetter(0), reverse=True)
	unique_meshdict = sorted(unique_meshdict.iteritems(), key=operator.itemgetter(0), reverse=True)
	unique_meshnet = sorted(unique_meshnet.iteritems(), key=operator.itemgetter(0), reverse=True)
	for q in range(0,len(mesh_dict)):
		mesh_dict[q]+=(unique_meshdict[q][1],)
		mesh_dict[q]+=(unique_meshnet[q][1],)
	mesh_dict.sort(key = operator.itemgetter(2,1), reverse=True)
	
	
	
	final=[]
	final.append(disease_list)
	final.append(mesh_dict)
	final.append(genes_list)
	final.append(all_dict)
	
	
	
	with open ('merge.txt','w') as data3:
		for s in range(0,min(75,len(mesh_dict))):
			for item in mesh_dict[s][3]:
				print >>data3, mesh_dict[s][0]+',', str(mesh_dict[s][1])+',', str(item)+'\r\n'
	
	
	return final,numabs,descrip

	
def disp_abs(request, start=20):
	genes = request.GET['genes']
	genes=genes.split(', ')
	count2=0
	abs_dict={}
	abs_list=[]
	term_list=[]
	list=[]
	term=False
	term_str=''
	if 'item' in request.GET and request.GET['item']:
		list = request.GET.getlist('item')
		term_str=' AND '.join(list)
	if 'item2' in request.GET:
		list = request.GET['item2']
		if len(list)==0:
			list=''
		list=list.split(', ')
		term_str= ' AND '.join(list)
	count2=0
	total=0
	for g in genes:
		try:				
			search_results = Entrez.read(Entrez.esearch(db="pubmed",
						term=g+" AND "+term_str, reldate=36500, date="pdat",
						usehistory="y"))
		except RuntimeError:
			pass
		
		try:
			handle = Entrez.efetch(db="pubmed",
									rettype="medline", retmode="text",
									retmax=10000, restart=int(start),
									webenv=search_results["WebEnv"],
									query_key=search_results["QueryKey"])
									
		except(KeyError, urllib2.HTTPError, httplib.IncompleteRead):
			pass

		total=total+int(search_results['Count'])
		
		try:
			records = Medline.parse(handle)
		except UnboundLocalError:
			pass
		
		print "Finding most applicable abstracts . . ."
		for record in records:
			rec=0
			rec2=0
			try:
				abstract=record['AB']
				id = record['PMID']
			except KeyError:
				continue
			count2 +=1
			
			for item in genes:
				if " "+item in abstract:
					rec += 1
				rec2+=abstract.count(item)
				
			for item in list:
				if " "+item in abstract:
					rec += 1
				rec2+=abstract.count(item)
				
			abs_dict[id]=(rec,rec2)

	abs_dict = sorted(abs_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
	
	ids=[x[0] for x in abs_dict]
	
	ids=ids[0:start]
	
	
	
	try:
		handle2 = Entrez.efetch(db="pubmed", rettype="medline", retmode="text",id=ids)								
	except(KeyError, urllib2.HTTPError, httplib.IncompleteRead):
		pass

	records3 = Medline.parse(handle2)
	
	print "Rendering abstracts . . ."
	for record in records3:
		words_found=[]
		rec=0
		rec2=0
		try:
			abstract=record['AB']
			author = record['AU']
			title= record['TI']
			title=title.replace('[',"")
			title=title.replace(']',"")
			pmid = record['PMID']
			journal = record['JT']
			date = record['DP']
		except KeyError:
			continue
		count2 +=1
		
		
		
		for item in genes:
			if re.search(r"\s"+item+"\d*(?![A-Z])", abstract):
				words_found.append(item)
			abstract=re.sub(r"\s"+item+"\d*(?![A-Z])"," <strong><u>"+item+"</u></strong>", abstract, flags=re.IGNORECASE)
			
		for item in list:
			if re.search(r"\s"+item+"\d*(?![A-Z])", abstract):
				words_found.append(item)
			abstract=re.sub(r"\s"+item+"\d*(?![A-Z])"," <strong><u>"+item+"</u></strong>", abstract, flags=re.IGNORECASE)
		
		
		handle4 = Entrez.elink(dbfrom="pubmed", id= pmid, cmd="llinks")
		record2 = Entrez.read(handle4)
		
		
		try:
			link = record2[0]['IdUrlList']['IdUrlSet'][0]['ObjUrl'][0]['Url']
		except IndexError:
			link='https://www.google.com'
		

		abs_list.append([title, author, abstract, link, journal, date, words_found, len(words_found)])
	
	abs_list.sort(key = operator.itemgetter(7,5), reverse= True)
		
	return render (request, 'disp_abs.html',
	{'abs':abs_list, 'genes':genes,'item':list, 'total':total,
	'shown':len(ids)})

def more_abs(request):
	if 'shown' in request.GET:
		shown = int(request.GET['shown'])
		return disp_abs(request, start=int(shown))
	else:
		return render (request, 'search_form.html', {'error': True})
		
def update_database(genes):
	for gene in genes:
		with open(gene+'.txt') as f:
			seem = [f.next() for x in xrange(100)]
			seem1=[]
			for item in seem:
				item=item.rstrip('\r\n')
				item=item.rstrip('\n')
				item=item.split(', ')
				seem1.append(item[1])

		for entry in seem1:
			pass

def robots(request):
	return render(request, 'robots.txt')

import simplejson
	
def visualize (request):
	genes = request.GET['genes']
	genes=genes.split(', ')
	genes = [x.upper() for x in genes]
	genes_new=[]
	for gene in genes:
		try:
			with open(gene+".txt"): genes_new.append(gene)
		except IOError:
			continue
				
	final,numabs,descrip=create_data(genes)
	final1=[]
	for item in final:
		final1.append(item[0:40])
	
	
	# abs=[]
	# for a in final1[0]:
		
		# for gene in genes:
			# abs_string=a[0] + ' AND '
			# abs_string += gene
			
			# try:				
				# search_results = Entrez.read(Entrez.esearch(db="pubmed",
							# term=abs_string, reldate=30, date="pdat",
							# usehistory="y"))
			# except RuntimeError:
				# pass
			
			# try:
				# handle = Entrez.efetch(db="pubmed",
										# rettype="medline", retmode="text",
										# retmax=1, 
										# webenv=search_results["WebEnv"],
										# query_key=search_results["QueryKey"])
										
			# except(KeyError, urllib2.HTTPError, httplib.IncompleteRead):
				# pass
				
			# try:
				# records = Medline.parse(handle)
			# except UnboundLocalError:
				# pass
			
			# print "Finding most applicable abstracts . . ."
			# for record in records:

				# try:
					# author = record['AU']
					# title= record['TI']
					# title=title.replace('[',"")
					# title=title.replace(']',"")
					# pmid = record['PMID']
					# journal = record['JT']
					# date = record['DP']
				# except KeyError:
					# continue
				
				
				# abs.append([a[0],author,title,pmid,journal,date])
	
	# abs2=[]
	# for a in final1[2]:
		
		# for gene in genes:
			# abs_string2=a[0] + ' AND '
			# abs_string2+= gene
			# try:				
				# search_results = Entrez.read(Entrez.esearch(db="pubmed",
							# term=abs_string2, reldate=365, date="pdat",
							# usehistory="y"))
			# except RuntimeError:
				# pass
			
			# try:
				# handle = Entrez.efetch(db="pubmed",
										# rettype="medline", retmode="text",
										# retmax=1, 
										# webenv=search_results["WebEnv"],
										# query_key=search_results["QueryKey"])
										
			# except(KeyError, urllib2.HTTPError, httplib.IncompleteRead):
				# pass
				
			# try:
				# records = Medline.parse(handle)
			# except UnboundLocalError:
				# pass
			
			# print "Finding most applicable abstracts . . ."
			# for record in records:

				# try:
					# author = record['AU']
					# title= record['TI']
					# title=title.replace('[',"")
					# title=title.replace(']',"")
					# pmid = record['PMID']
					# journal = record['JT']
					# date = record['DP']
				# except KeyError:
					# continue
					
				# abs2.append([a[0],author,title,pmid,journal,date])
				
	json_final = simplejson.dumps(final1)
	json_genes = simplejson.dumps(genes_new)
	
	return render (request, 'netvisual.html', {'final':json_final, 'genes':json_genes, 'final1':final1,'genes1':genes_new,'descrip':descrip})
	