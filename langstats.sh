#!/bin/bash
dir=$1
if [ "$dir" == "" ]; then
	echo "Directory to stat languages? (hit enter to use CWD)"
	read dir
	if [ "$dir" == "" ]; then
		dir="$PWD"
	fi
fi

#get list of all files in directory
files=$(find $dir -type f)
#get count of all files in directory
cnt_all=$(echo "$files" | wc -l)

#count files for each language
cnt_asm=$(	echo "$files" | grep -io \
	"\.asm$" \
| wc -l)
cnt_c=$(	echo "$files" | grep -io \
	"\.c$\|\.h$" \
| wc -l)
cnt_css=$(	echo "$files" | grep -io \
	"\.css$\|\.less$" \
| wc -l)
cnt_cpp=$(	echo "$files" | grep -io \
	"\.cpp$\|\.hpp$" \
| wc -l)
cnt_dos=$(	echo "$files" | grep -io \
	"\.dos$\|\.bat$\|\.cmd$" \
| wc -l)
cnt_html=$(	echo "$files" | grep -io \
	"\.html$\|\.htm$" \
| wc -l)
cnt_java=$(	echo "$files" | grep -io \
	"\.java$" \
| wc -l)
cnt_js=$(	echo "$files" | grep -io \
	"\.js$" \
| wc -l)
cnt_pl=$(	echo "$files" | grep -io \
	"\.pl$" \
| wc -l)
cnt_php=$(	echo "$files" | grep -io \
	"\.php$\|\.phar$" \
| wc -l)
cnt_ps=$(	echo "$files" | grep -io \
	"\.ps$" \
| wc -l)
cnt_py=$(	echo "$files" | grep -io \
	"\.py$" \
| wc -l)
cnt_rb=$(	echo "$files" | grep -io \
	"\.rb$" \
| wc -l)
cnt_sh=$(	echo "$files" | grep -io \
	"\.sh$" \
| wc -l)

rt_asm=$(	bc -l <<< "($cnt_asm	/ $cnt_all)")
	pc_asm=$(	printf "%.2f" "`bc -l <<< "($rt_asm * 100)"`")
rt_c=$(		bc -l <<< "($cnt_c		/ $cnt_all)")
	pc_c=$(		printf "%.2f" "`bc -l <<< "($rt_c * 100)"`")
rt_css=$(	bc -l <<< "($cnt_css	/ $cnt_all)")
	pc_css=$(	printf "%.2f" "`bc -l <<< "($rt_css * 100)"`")
rt_cpp=$(	bc -l <<< "($cnt_cpp	/ $cnt_all)")
	pc_cpp=$(	printf "%.2f" "`bc -l <<< "($rt_cpp * 100)"`")
rt_dos=$(	bc -l <<< "($cnt_dos	/ $cnt_all)")
	pc_dos=$(	printf "%.2f" "`bc -l <<< "($rt_dos * 100)"`")
rt_html=$(	bc -l <<< "($cnt_html	/ $cnt_all)")
	pc_html=$(	printf "%.2f" "`bc -l <<< "($rt_html * 100)"`")
rt_java=$(	bc -l <<< "($cnt_java	/ $cnt_all)")
	pc_java=$(	printf "%.2f" "`bc -l <<< "($rt_java * 100)"`")
rt_js=$(	bc -l <<< "($cnt_js		/ $cnt_all)")
	pc_js=$(	printf "%.2f" "`bc -l <<< "($rt_js * 100)"`")
rt_pl=$(	bc -l <<< "($cnt_pl		/ $cnt_all)")
	pc_pl=$(	printf "%.2f" "`bc -l <<< "($rt_pl * 100)"`")
rt_php=$(	bc -l <<< "($cnt_php	/ $cnt_all)")
	pc_php=$(	printf "%.2f" "`bc -l <<< "($rt_php * 100)"`")
rt_ps=$(	bc -l <<< "($cnt_ps		/ $cnt_all)")
	pc_ps=$(	printf "%.2f" "`bc -l <<< "($rt_ps * 100)"`")
rt_py=$(	bc -l <<< "($cnt_py		/ $cnt_all)")
	pc_py=$(	printf "%.2f" "`bc -l <<< "($rt_py * 100)"`")
rt_rb=$(	bc -l <<< "($cnt_rb		/ $cnt_all)")
	pc_rb=$(	printf "%.2f" "`bc -l <<< "($rt_rb * 100)"`")
rt_sh=$(	bc -l <<< "($cnt_sh		/ $cnt_all)")
	pc_sh=$(	printf "%.2f" "`bc -l <<< "($rt_sh * 100)"`")

echo "total files:      $cnt_all"
echo "-----------------------------------------"

langs="`\
if (( "$cnt_asm" > "0" )); then
	echo "Assembly:         $cnt_asm ($pc_asm%)"
fi
if (( "$cnt_c" > "0" )); then
	echo "C:                $cnt_c ($pc_c%)"
fi
if (( "$cnt_cpp" > "0" )); then
	echo "C++:              $cnt_cpp ($pc_cpp%)"
fi
if (( "$cnt_css" > "0" )); then
	echo "CSS:              $cnt_css ($pc_css%)"
fi
if (( "$cnt_dos" > "0" )); then
	echo "DOS:              $cnt_dos ($pc_dos%)"
fi
if (( "$cnt_html" > "0" )); then
	echo "HTML:             $cnt_html ($pc_html%)"
fi
if (( "$cnt_java" > "0" )); then
	echo "Java:             $cnt_java ($pc_java%)"
fi
if (( "$cnt_js" > "0" )); then
	echo "JavaScript:       $cnt_js ($pc_js%)"
fi
if (( "$cnt_pl" > "0" )); then
	echo "Perl:             $cnt_pl ($pc_pl%)"
fi
if (( "$cnt_php" > "0" )); then
	echo "PHP:              $cnt_php ($pc_php%)"
fi
if (( "$cnt_ps" > "0" )); then
	echo "PowerShell:       $cnt_ps ($pc_ps%)"
fi
if (( "$cnt_py" > "0" )); then
	echo "Python:           $cnt_py ($pc_py%)"
fi
if (( "$cnt_rb" > "0" )); then
	echo "Ruby:             $cnt_rb ($pc_rb%)"
fi
if (( "$cnt_sh" > "0" )); then
	echo "Shell:            $cnt_sh ($pc_sh%)"
fi
`"

echo "`echo "$langs" | sort -k2 -n --reverse`"

exit

