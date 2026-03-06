mkdir -p not_clipped
awk '{
  hap=$4;
  split(hap,a,"#");
  name=a[1];
  if(a[2]=="1") tag="primary";
  else if(a[2]=="2") tag="alternate";
  else tag=a[2];
  fn="hap_beds/" name "_" tag ".bed";
  print > fn
}' walks.bed
