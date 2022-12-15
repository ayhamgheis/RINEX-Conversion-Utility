#!/bin/bash
for i in ./*.tgd;
        do ./ConvertRinex -in "$i" "-station" "cref" "-qc"> test.txt;
	done
~                    
