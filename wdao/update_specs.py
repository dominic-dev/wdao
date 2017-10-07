#!/usr/bin/python3
import glob
from tqdm import tqdm

import core.data
import core.forms as forms

MIN_N_DATA = None # Minimal number of harvests required to base new range on

# Get spec files
spec_files = glob.glob('../SPC/SPC*')
spec_files += glob.glob('../SPC/spc*')

# Update files
data = []
for f in tqdm(spec_files):
  s = forms.Spec(f)
  line = s.update(data='output/geordende_oogsten_bereik_gem.csv', min_n=MIN_N_DATA)
  if line: data.append(line)

# Save rapport
d = core.data.Data()
d.data = data
output = 'output/SPEC_bestanden_veranderingen.csv'
d.save_data_to_csv(output)

print('Finished. Changed {} of {} files.'.format(len(spec_files)-len(forms.Spec.not_found), len(spec_files)))

if forms.Spec.not_found:
  print('For {} files, no valid data was found. {:.2f}%'.format(len(forms.Spec.not_found), len(forms.Spec.not_found)/len(spec_files) * 100))
  print('These files are')
  [print(f) for f in forms.Spec.not_found]

if forms.Spec.not_enough_data:
  print('For {} files, not enough data was available to base a new period on. {:.2f}%'.format(len(forms.Spec.not_enough_data), len(forms.Spec.not_enough_data)/len(spec_files) *100))
  print('These files are')
  [print(f) for f in forms.Spec.not_enough_data]


print("Rapport saved to {}".format(output))
