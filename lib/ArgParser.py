import argparse
import sys
#Oscillation variables that will be measured by SNO+/vary
#between SuperK and KamLAND; fixed parameters are found hard-coded in
#./lib/NuSPectrum.py


parser = argparse.ArgumentParser(description='Python-based software for determining and '+\
        ' logging the charge gains of PMTs')
parser.add_argument("--debug",action="store_true")
parser.add_argument("-d", "--database",action="store",dest="DB",
                  type=str,
                  help="Specify the JSON file to either analyze or append fits to")
parser.add_argument("-a", "--append",action="store",dest="APPEND",
                  type=str,
                  help="Path to a ROOT file holding new charge information for tubes")

parser.set_defaults(DB="./DB/TransparencyRuns.json",APPEND=None,debug="False")
args = parser.parse_args()
DB = args.DB
APPEND = args.APPEND
DEBUG = args.debug

