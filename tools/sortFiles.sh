for file in ../captured/chileSearch.csv
do
echo "${file##*/}"
sort -k2,2 $file > ${file##*/}
done