import core.data as data

def main():
  d = data.Data()
  d.collect_from_csv('output/geordende_oogsten_jaar.csv')
  d.range_and_average()

if __name__ == '__main__':
  main()
