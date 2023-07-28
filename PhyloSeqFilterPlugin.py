import PyPluMA


class PhyloSeqFilterPlugin:
    def input(self, filename):
      self.parameters = dict()
      paramfile = open(filename, 'r')
      for line in paramfile:
         contents = line.split('\t')
         self.parameters[contents[0]] = contents[1].strip()

      self.otu_file = open(PyPluMA.prefix()+"/"+self.parameters["OTU"], 'r')
      self.tax_file = open(PyPluMA.prefix()+"/"+self.parameters["TAX"], 'r')
      sample_file =open(PyPluMA.prefix()+"/"+self.parameters["META"], 'r')
      self.threshold = float(self.parameters["threshold"])
      if ("keepifone" in self.parameters):
          self.keepifone = True
      else:
          self.keepifone = False
      #Idea: Zero out (don't remove) OTUs in less than 50% of a category set
      # Then once everything is done, remove those with zero over all samples

      sample_file.readline()
      cur_sample = "BLAH"
      cur_sample_idx = -1
      self.categories = [-1]
      for line in sample_file:
         contents = line.strip().split(",")
         if (contents[1] != cur_sample):
             cur_sample = contents[1]
             cur_sample_idx += 1
         self.categories.append(cur_sample_idx)
    def run(self):
       pass

    def output(self, filename):
      otu_filter_file = open(filename+"/"+self.parameters["OTUFilter"], 'w')
      otu_filter_file.write(self.otu_file.readline())

      toRemove = []
      for line in self.otu_file:
          contents = line.strip().split(',')
          contents2 = contents.copy()
          for i in range(0, len(contents)):
              #print(i)
              cat = self.categories[i]
              if (cat != -1):
                  if (cat != oldcat):
                      if ((cat != 0) and (numkittens/numcats < (self.threshold/float(100)))):
                          # Walk backwards, zero out
                          j = i-1
                          while (self.categories[j] == oldcat):
                              contents[j] = str(0)
                              j -= 1
                      #elif (cat != 0):
                          #print("KEEPING: "+str(numkittens)+" "+str(numcats)+" "+str(cat)+" "+str(oldcat))
                      numkittens = 0.0
                      numcats = 0.0
                      if (float(contents[i]) != 0):
                         numkittens += 1.0
                      numcats += 1.0
                  else:
                      if (float(contents[i]) != 0):
                         numkittens += 1.0
                      numcats += 1.0
              oldcat = cat
          # One final time
          if (numkittens/numcats < (self.threshold/float(100))):
             j = len(contents)-1
             while (self.categories[j] == oldcat):
                contents[j] = str(0)
                j -= 1
          #else:
          #   print("KEEPING: "+str(numkittens)+" "+str(numcats))

          # If all are zero, add to remove set
          zeroFlag = True
          for i in range(1, len(contents)):
              if (float(contents[i]) != 0):
                 zeroFlag = False
          if (zeroFlag):
              toRemove.append(contents[0])
              #print("REMOVING "+contents[0])
          else:
              for i in range(0, len(contents)):
                if (self.keepifone):
                   otu_filter_file.write(contents2[i])
                else:
                   otu_filter_file.write(contents[i])
                if (i == len(contents)-1):
                  otu_filter_file.write('\n')
                else:
                  otu_filter_file.write(',')
      
      
      
      tax_filter_file = open(filename+"/"+self.parameters["TAXFilter"], 'w')
      tax_filter_file.write(self.tax_file.readline()) #Header
      
      
      for line in self.tax_file:
          line = line.strip()
          contents = line.split(',')
      
          if (contents[0] not in toRemove):
              tax_filter_file.write(line+"\n")

