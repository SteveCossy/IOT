# Based on https://stackoverflow.com/questions/10929453/read-a-file-line-by-line-assigning-the-value-to-a-variable
#  ... and https://stackabuse.com/substrings-in-bash/
#  ... and https://www.cyberciti.biz/faq/unix-linux-bsd-appleosx-bash-assign-variable-command-output/

while IFS= read -r line || [[ -n "$line" ]]; do
    Library=$(echo $line | cut -d'=' -f 1)
#    grep -n `echo $Library` *
    echo $Library
done < "$1"
