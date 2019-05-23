DIR=`dirname "$0"`
HERE=`realpath "$DIR"`

cp $HERE/../hermione.conf.dist $HERE/../hermione.conf
cp $HERE/../hermione_env.sh.dist $HERE/../hermione_env.sh

PATT="s/<USER>/$USER/g"
sed -i -e $PATT $HERE/../hermione.conf.dist