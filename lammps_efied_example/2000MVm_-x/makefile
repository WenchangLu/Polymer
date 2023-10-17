LSF_JOBS = `grep submitted .jobid std.oe?????? | cut -d'<' -f 2 | cut -d'>' -f 1 | grep -v lmp` `ls std.oe?????? | cut -b 7-12`

clean:
	rm .jobid core.* init*.lmpdata final*.lmpdata dump.* *.lammps restart*lmp std.oe[0-9]*[0-9]

jsrun:
	bash -x jsrun.lsf &

submit:
	bsub jobfile >> .jobid

killall:
	bkill $(LSF_JOBS)
