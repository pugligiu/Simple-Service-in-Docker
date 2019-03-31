pip install -r ./requirements.txt

if [ $? -ne 0 ]
then
  	exit -1
fi

res=`python3 -m unittest discover -s ./src -p "*_test.py"`

if [ $? -ne 0 ]
then
	printf '%s\n' "Unit test is failed. Run your unit test" >&2
  	exit -1
fi
