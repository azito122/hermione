C=$1
V=$2
T=$3

if [[ "$C" =~ ^(remember|rem|r|add|a|store)$ ]];
then
    echo "remembering..."
    python3 remember.py "$V"
elif [[ "$C" =~ ^(recall|rc|view|v|find|f|search|s)$ ]];
then
    if [[ "$V" =~ ^(-t|--tag)$ ]];
    then
        echo "recalling tag..."
        python3 recall.py "#$T"
    else
        echo "recalling..."
        python3 recall.py "$V"
    fi
fi