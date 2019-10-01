for file in ../earthquakes/*
do
echo "${file##*/}"
sort -k2,2 $file > ${file##*/}
done