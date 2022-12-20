import sys
import PyIO
import PyPluMA

class Unique2OnePlugin:
    def input(self, filename):
        self.parameters = PyIO.readParameters(filename)
    def run(self):
      abund = open(PyPluMA.prefix()+"/"+self.parameters["abundances"], 'r')
      metadata = open(PyPluMA.prefix()+"/"+self.parameters["metadata"],'r')

      categories = dict()
      metadata.readline()
      groups = set()
      for line in metadata:
          contents = line.strip().split(',')
          categories[contents[0]] = contents[1]
          groups.add(contents[1])

      firstline = abund.readline()
      taxa = firstline.strip().split(',')
      #taxa = taxa[1:]

      self.counts = dict()
      for i in range(1, len(taxa)):
          self.counts[taxa[i]] = dict()
          for group in groups:
             self.counts[taxa[i]][group] = 0


      for line in abund:
          contents = line.strip().split(',')
          sample = contents[0]
          for pos in range(1, len(contents)):
              self.counts[taxa[pos]][categories[sample]] += float(contents[pos])

    def output(self, filename):
      outfile = open(filename, 'w')
      for key in self.counts:
          for key2 in self.counts[key]:
              if (self.counts[key][key2] == 0):
                  for key3 in self.counts[key]:
                      if (self.counts[key][key3] != 0):
                          outfile.write(key+" IS UNIQUE TO: ")
                          outfile.write(key3+"\n")
