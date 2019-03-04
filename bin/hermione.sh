C=$1
V=$2
T=$3

HERE="$HOME/hermione/bin"

if [[ "$C" =~ ^(remember|rem|r|add|a|store)$ ]];
then
    if [ "$V" = "" ];
    then
        echo "" > /tmp/hermione
        vim /tmp/hermione
        MEM=$(cat /tmp/hermione)
        python3 $HERE/remember.py "$MEM"
    else
        echo "remembering..."
        python3 $HERE/remember.py "$V"
    fi
elif [[ "$C" =~ ^(recall|rc|view|v|find|f|search|s)$ ]];
then
    if [[ "$V" =~ ^(-t|--tag)$ ]];
    then
        echo "recalling tag..."
        python3 $HERE/recall.py "#$T"
    else
        echo "recalling..."
        python3 $HERE/recall.py "$V"
    fi
elif [[ "$C" =~ ^(edit|e)$ ]];
then
    ID=$(python3 $HERE/edit.py "$V")
    vim /tmp/hermione
    MEM=$(cat /tmp/hermione)
    bash $HERE/hermione.sh reremember "$MEM" "$ID"
# elif [[ "$C" =~ ^(reremember|rr)$ ]];
# then
#     python3 $HERE/remember.py "$V" "$T"
elif [[ "$C" =~ ^(delete|d|forget|fg) ]];
then
    python3 $HERE/forget.py "$2"
    echo "memory #$2 is forgotten"
fi