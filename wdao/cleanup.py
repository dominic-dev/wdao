import shutil

def main():
  answer = ''
  while answer.lower() not in ('y', 'yes', 'n', 'no'):
    answer = input("All files in /tmp will be deleted, continue? (y)es or (n)o?\n")

  if answer[0].lower() == 'n':
    exit()
  else:
    cleanup()

def cleanup():
  try:
    shutil.rmtree('tmp')
  except FileNotFoundError:
    pass
  print('Finished.')

if __name__ == '__main__':
  main()
