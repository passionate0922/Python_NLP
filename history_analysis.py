#!/usr/bin/python

import os, sys
import csv
from datetime import date
import string
from string import punctuation

path = "/afs/cs.wisc.edu/u/n/a/nam/Roots/medical_history"
pinfo = []
general_health = ['general', 'chest', 'abdonimal', 'cramp', 'abscess', 'acid', 'cough', 'diarrhea', 'sore', 'throuat','fever','otalgia', 'headache', 'abdominal']
sexual_health = ['sexual', 'vagina', 'hiv', 'hepatitis','trichomoniasis']

with open('patient_info.csv','wb') as csvfile:
   infowriter = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
   infowriter.writerow(['filename', 'Name', 'DOB', 'AIDS/HIV', 'Allergies', 'Allergy Details', 'Asthma', 'Back Trouble', 'Bleeding Disease', 'Surgery', 'Surgery Details', 'Liver Disease', 'Fainting', 'Result'])
   for file in os.listdir(path):
      print file
      history = open(path+"/"+file).read()

      #Split the medical history file line by line
      history_line = history.split('\n')
      new_hl = []
      for line in history_line:
         if line.strip():
            new_hl.append(line)
      
      #Obtain patient's personal information
      for content in new_hl[0:2]:
         personalinfol = content.split(' = ')
         pinfo.append(personalinfol[1])
    

      #Analyze medical symptom
      for punc in list(punctuation):
         medical_symptom = new_hl[3].lower().translate(None, string.punctuation)
         medical_symptom = medical_symptom.split(' ')
         symp = []
         for i in medical_symptom:
             if i.strip():
                symp.append(i)
      
      #Based on symptoms, determine which disease-category that symptoms fit in
      result_a = ' '
      result_b = ' '
      result_c = 'Complex'
      result_d = ' '
      for word in symp:
          if word in general_health:
             result_a = 'General Health'
             
          elif word in sexual_health:
             result_b = 'Sexual Health'

          else:
             result_d = 'Healthy'
      
      if result_a.isspace():
          if result_b.isspace():
             if result_c.isspace():
                 pinfo.append(result_d)
             else:
                 pinfo.append(result_c)
          else:
             pinfo.append(result_b)
      else:
          if result_b.isspace():
             pinfo.append(result_a)
          else:
             pinfo.append(result_c)
        

      #Analyze medical history
      for content in new_hl[5:13]:
         medicalhistory = content.split(' : ')
         pinfo.append(medicalhistory[1])
      
     # No allergy
      if pinfo[4] == 'n':
         if pinfo[8] == 'n':
            infowriter.writerow([file, pinfo[0],pinfo[1],pinfo[3],pinfo[4],'None',pinfo[5], pinfo[6],pinfo[7],pinfo[8], 'None', pinfo[9], pinfo[10], pinfo[2]])
            pinfo = []
         else:# pinfo[7] == 'y':
            detail_surgery = new_hl[14]
            infowriter.writerow([file, pinfo[0],pinfo[1],pinfo[3],pinfo[4],'None',pinfo[5], pinfo[6],pinfo[7],pinfo[8], detail_surgery, pinfo[9], pinfo[10], pinfo[2]])
            pinfo = []
     # Yes to allergy
      else:
         if pinfo[8] == 'n':
            detail_allergy = new_hl[17]
            infowriter.writerow([file, pinfo[0],pinfo[1],pinfo[3],pinfo[4],detail_allergy,pinfo[5], pinfo[6],pinfo[7],pinfo[8], 'None', pinfo[9], pinfo[10], pinfo[2]])
            pinfo = []
         else:
            detail_allergy = new_hl[18]
            infowriter.writerow([file, pinfo[0],pinfo[1],pinfo[3],pinfo[4], detail_allergy, pinfo[5], pinfo[6],pinfo[7],pinfo[8], detail_surgery, pinfo[9], pinfo[10], pinfo[2]])
            pinfo = []
