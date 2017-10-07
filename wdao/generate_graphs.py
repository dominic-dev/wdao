#!/user/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import pickle

from decimal import Decimal
# Multipage pdf support
from matplotlib.backends.backend_pdf import PdfPages
# Progress bar
from tqdm import tqdm

from core.data import Data
from core.helpers import create_incremented_filename

def main():
  d = Data()
  d.collect_from_csv('output/geordende_oogsten_jaar.csv')

  filename = create_incremented_filename('output/graphs_multiple.pdf')
  with PdfPages(filename) as pdf:
    for line in tqdm(d.data):
      name = ' '.join(line[:2])
      # Load date year pairs [decimal_date, year]
      date_year_pairs = [l.strip().split('#') for l in line[2:] if (l.strip() not in ('', '\n', '0', 0))]

      # Ignore empty rows
      if not date_year_pairs:
        continue

      # Separate pairs into two lists
      x = [float(v[1]) for v in date_year_pairs] # Years
      y = [float(v[0]) for v in date_year_pairs] # Decimal dates


      plt.figure()
      # Scatter plot
      plt.scatter(x, y, c='#0000ff')
      # Regression line
      fit = np.polyfit(x, y, deg=1)
      fit_fn = np.poly1d(fit)
      plt.plot(x, fit_fn(x), '--k', color='red')
      #plt.axis([0, 13, int(min(dates), int(max(dates)))])
      y_mean = int(np.mean(y).round())
      plt.yticks(range(y_mean-3, y_mean+3))
      #plt.xticks(range(len(dates)))
      plt.xticks(range(2005, 2018))
      plt.ylabel('Months')
      plt.xlabel('Harvests')
      plt.title(name)
      pdf.savefig()

#  with PdfPages('output/graphs_combined.pdf') as pdf:
#    plt.figure()
#
#    i = range(1, len(d.data)+1)
#    for line in tqdm(d.data):
#      name = ' '.join(line[:2])
#      # Load date year pairs [decimal_date, year]
#      date_year_pairs = [l.strip().split('#') for l in line[2:] if (l not in ('', '\n', '0'))]
#      # Separate pairs into two lists
#
#      x = [float(v[1]) for v in date_year_pairs] # Years
#      y = [float(v[0]) for v in date_year_pairs] # Decimal dates
#
#
#      # Scatter plot
#      plt.scatter(x, y, c=i, cmap=plt.cm.hsv)
#
#    plt.yticks(range(13))
#    plt.xticks(range(2005, 2018))
#    plt.ylabel('Maanden')
#    plt.xlabel('Jaren')
#    plt.title('Weleda NL Oogsten')
#    pdf.savefig()

if __name__ == '__main__':
  main()
