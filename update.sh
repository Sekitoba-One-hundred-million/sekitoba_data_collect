declare -a array=( #"main_data_collect.py"
                   "baba_index_get.py"
                   "blood_data_get.py"
                   "corner_rank_collect.py"
                   "parent_data_collect.py"
                   "race_course_data.py"
                   "race_info_collect.py"
                   "race_time_collect.py"
                   "time_index_get.py"
                   "train_data_collect.py"
                   "wrap_data_collect.py"
                   "jockey_id_collect.py"
                   "jockey_full_data_collect.py" )

log_name="progress.txt"

rm -rf $log_name

for f in "${array[@]}"; do
    python $f
    echo "finish " $f >> $log_name
done
exit 0

#race_up_halon.py
