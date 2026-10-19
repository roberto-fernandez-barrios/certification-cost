"""Verify immutable inputs, copy to a NEW directory, run existing checkers."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def main()->None:
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 manifest=json.loads((HERE/'INPUT_MANIFEST.json').read_text(encoding='utf8'))
 for rel,item in manifest.items():
  if sha(HERE/rel)!=item['sha256']:raise ValueError('Input mismatch: '+rel)
 dest=a.output.resolve()
 if dest==HERE or HERE in dest.parents:raise ValueError('Choose a NEW directory outside this package')
 dest.mkdir(parents=True,exist_ok=False)
 for rel in manifest:
  p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(HERE/rel,p)
 records=[];py=[sys.executable,'-B','-X','utf8']
 commands=[['independent_checks.py',p] for p in ['bellman','box','profiles','tail']]+[['independent_factory.py']]
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
 for i,command in enumerate(commands,1):
  start=time.perf_counter()
  p=subprocess.run(py+command,cwd=dest,env=env,capture_output=True,text=True,encoding='utf8',timeout=180)
  log=f'{i:02d}.log';(dest/log).write_text(p.stdout+p.stderr,encoding='utf8')
  records.append({'command':['python','-B','-X','utf8',*command],'exit_code':p.returncode,'seconds':time.perf_counter()-start,'log':log})
  report={'python':sys.version,'commands':records,'status':'IN_PROGRESS'}
  (dest/'EXECUTION_RECORD.json').write_text(json.dumps(report,indent=2),encoding='utf8')
  print(i,command,'exit',p.returncode,flush=True)
  if p.returncode:raise SystemExit(p.returncode)
 for rel,item in manifest.items():assert sha(dest/rel)==item['sha256'],rel
 report['status']='COMPLETED';report['input_files_unchanged']=len(manifest)
 report['scope']='Existing deterministic mathematical checks; no simulation, no runtime certification, no human review.'
 (dest/'EXECUTION_RECORD.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
if __name__=='__main__':main()
