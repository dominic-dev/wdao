import os
from calendar import monthrange
from decimal import Decimal, getcontext


class DateRange:
  """Create a string from a date range (e.g. juni - augustus)
    Arguments:
      begin (float): Starting month in decimal
      end (float): Ending month in decimal.
  """

  months = (
    '',
    'januari',
    'februari',
    'maart',
    'april',
    'mei',
    'juni',
    'juli',
    'augstus',
    'september',
    'oktober',
    'november',
    'december'
  )

  def __init__(self, dates, mode='min_max'):
    #dates = [float(d) for d in dates]
    self.dates = dates
    self.mode = mode


  def _dec_as_str(self, date):
    """Convert decimal date to string"""
    month = self.months[int(date)]
    dec_remainder = date - int(date)

    if dec_remainder > 0.7:
      month = 'eind ' + month
    if dec_remainder < 0.23:
      month = 'begin ' + month
    return month

  def _mean_as_str(self):
    """
    Return mean of date range as string. E.g. 'begin juni'
    """
    return self._dec_as_str(sum(self.dates) / len(self.dates))

  def _range_as_str(self):
    """ Return range of dates as string
    E.g. 'begin juni - eind mei'
    """
    _min = min(self.dates)
    _max = max(self.dates)
    if int(_min) == int(_max):
      return self.months[int(_min)]
    return self._dec_as_str(_min) + ' - ' + self._dec_as_str(_max)

  @property
  def as_str(self):
    """Return string from date range"""
    if self.mode == 'ave':
      return self._mean_as_str()
    else:
      return self._range_as_str()


def numerize_date(date, include_year=False):
  """
  Take date in month day format, return numerized date in decimal
  Arguments:
    date (tuple): Date to process,format (year, month, day)
  """
  # Convert day to decimal of month
  year, month, day = date
  # If date is valid
  if month in range(1,13):
    n_days = monthrange(year, month)[1]
    getcontext().prec = 3
    dec_day = Decimal(day / n_days)
    if include_year:
      return "{:.2f}#{}".format(month+dec_day, year)
    else:
      return month + dec_day
  # If date is invalid
  else:
    return 0


def create_incremented_filename(path):
  """ Take path, and add an incrementor if necessary at the end of filename
  until path is unique.

  Arguments:
    path (string): The path to filename

  """

  # Split path into directory/filename.extension
  directory, full_filename = os.path.split(path)
  filename, extension = os.path.splitext(full_filename)

  try:
    open(path)
  # If path does not exist.
  except FileNotFoundError:
    return path
  # If path does exist, add an incrementor at the end of filename.
  else:
    i = 2
    while True:
      path = os.path.join(directory, filename + str(i) + extension)
      try:
        open(path)
      except FileNotFoundError:
        return path
        break
      else:
        i += 1

