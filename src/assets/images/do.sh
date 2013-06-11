
python makeFeed.py -r $1
echo "lst count "
wc -l $1/$1.lst
echo "jpg file count"
ls -l $1/*.jpg | wc -l
