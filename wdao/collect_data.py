#!/usr/bin/python3
import core.data as data

def main():
  d = data.Data()
  d.list_all_harvests()
  d.save_data_to_csv()
  d.order_harvests_by_year_and_plant(output='output/geordende_oogsten_jaar.csv', include_year=True)

if __name__ == '__main__':
  main()
