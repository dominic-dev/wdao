import csv
import os
import glob
import re
import scipy.stats
import subprocess

from collections import OrderedDict
from operator import itemgetter
from tqdm import tqdm
from pathlib import Path

from . import forms
from . import helpers


class Data:
  data = []
  """Data object that contains data"""

  def list_all_harvests(self, path=None):
    """Collect data from leveringsformulieren and list all harvests.
    Save to file. One row per harvest (code, full name, *[harvests])"""
    print("Collecting data from forms.")
    if path is None:
      # Go up two dirs and add trailing slash
      path = os.path.join(str(Path(__file__).parents[2]), '')

    # RegEx for the filename
    pattern = re.compile(r"""(\d\d)      # year
                             ([A-Za-z]+) # the plant code
                             (\d\d)      # the month
                             (\d\d)      # the day
                         """, re.IGNORECASE | re.VERBOSE)

    files = [g for g in glob.glob(path + '20??/*') if pattern.search(g)]
    # Reduce files to relevant files.
    files = [f for f in files if not 'teelt' in f]
    total = len(files)

    # Start processing files
    count = 0
    data = []
    for f in tqdm(files):
      # Get year, name and month from filename
      # <yy><name><mm><dd>
      y, name, m, d = pattern.search(f).groups()
      name = name.strip().lower()
      date = (int(y), int(m), int(d))

      # Initialize form
      form = forms.Form(f)
      # Append data if valid
      try:
        data.append([name, form.get_plant_name().replace(',', ''),\
                     form.get_plant_part().lower(), form.get_date()])
      except AttributeError:
        print('Could not process {}.'.format(f))
      else:
        count += 1

    print("Finished. Succesfully processed {} of {} files. {:.2f}%".format(count, total, count/total*100))
    type(self).data = data
    return self.data

  def order_harvests_by_year_and_plant(self, output='output/geordende_oogsten.csv', include_year=False):
    """ Take all harvests as self.data
    Return harvests ordered by plant/part and save to file."""

    # Collect data
    if not self.data:
      self.list_all_harvests()

    # Read data
    ordered_data = {}
    harvests_by_year = {}
    for line in self.data:
      code, name, part, date = line
      code = code.strip().lower()
      part = part.strip().lower()
      # Convert date dd-mm-yyyy to list of year, month, day integers
      date = [int(x) for x in date.strip().split('-')]
      date.reverse()
      year, month, day = date
      # Create separate lists of harvests per plant+part
      # Dates are written as decimal_date#year in the data.
      try:
        harvests_by_year.setdefault(year, {}).\
          setdefault(name + '#' + part, []).append(helpers.numerize_date(date, include_year))
      except TypeError:
        pass

    # Sort by year
    harvests_by_year = OrderedDict(sorted(harvests_by_year.items()))

    # Get median per harvest per year
    all_harvests = {}
    for year, harvests in harvests_by_year.items():
      for name, harvest in harvests.items():
        all_harvests.setdefault(name, []).append(
          harvest[len(harvest)//2]
        )

    # Write data
    # Split the key as k by # and unpack
    # unpack harvests as v
    data = [[*k.split('#'), *v] for k,v in all_harvests.items()]
    self.data = data
    self.save_data_to_csv(output)
    print("Harvests ordered by plant/part saved to {}".format(output))
    return self.data

  def range_and_average(self):
    """ Take all harvests as self.data
    Return harvests date range and average by plant/part
    and save to file."""
    if not self.data:
      self.order_harvests_by_year_and_plant()
    # Range and average per plant/part
    # Filter empty values and newlines
    filtered = ('', '\n')
    self.data = [[val for val in line if val not in filtered] for line in self.data]

    data = []
    for line in self.data:
      full_name, part = line[0:2]
      # The date is written as decimal_data#year e.g. 6.57#2012
      # Here only the date is used
      dates = [float(x.split('#')[0]) for x in line[2:]]
      date = helpers.DateRange(dates)
      data.append([full_name, part, date._range_as_str(), date._mean_as_str(), len(dates)])
    self.data = data
    output = 'output/geordende_oogsten_bereik_gem.csv'
    self.save_data_to_csv(output)
    print("Range and mean for harvests by plant/part saved to {}".format(output))

  def collect_from_csv(self, path='data.csv'):
    """Read data from .csv file"""
    # Only .csv accepted as source.
    if os.path.splitext(path)[1] != '.csv':
      raise TypeError("File format not accepted.")
    data = []
    # Read data
    with open(path) as f:
      for line in f.readlines():
        data.append(line.split(','))

    type(self).data = data
    return self.data

  def trend(self):
    if not self.data:
      self.order_harvests_by_year_and_plant()

    data = []
    for row in self.data:
      name, part = row[:2]
      dates = [float(x) for x in row[2:] if x != '' and x!= '\n']
      # Calculate correlation for the dates of the harvests, and the index of date c.q. the position in sequence
      # assuming the dates are ordered by year, which they are.
      x = [dates.index(d)+1 for d in dates]
      y = dates
      #correlation = numpy.corrcoef(x, y)[0][1]

      if len(dates) > 1:
        correlation = scipy.stats.pearsonr(x,y)[0]
        if correlation:
          slope = scipy.stats.linregress(x, y)[0]
          data.append([name, part, correlation, slope, len(dates)])

    # Sort by correlation
    data = sorted(data, key=itemgetter(2))
    self.data = data
    output = 'output/tendens.csv'
    self.save_data_to_csv(output)

  def save_data_to_csv(self, output='output/data.csv'):
    """Save data, if any, to csv"""
    if not self.data:
      return print("Nothing to save.")

    if not os.path.exists('output'):
      os.mkdir('output')

    with open(output, 'w') as f:
      wr = csv.writer(f)
      wr.writerows(self.data)
    return output

  def get_data(self):
    """ Collect the data. """
    if not self.data:
      try:
        self.collect_from_csv()
      except:
        self.collect_from_forms()
    return self.data
