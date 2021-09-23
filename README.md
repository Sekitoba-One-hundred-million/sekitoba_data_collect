# 赤兎馬のスクレイピングコード
全てのファイル単体で完結している。  
全てのファイルでpickleでAWSのS3に保存される。main_data_collect.pyが基準となっている。

## ファイルの説明
以下で各ファイルの説明と作成データの説明を行う。

### main_data_collect.py
2009~2020までのデータ収集を行う。  
ここで作成されるデータをベースに他のデータの収集を行う。

1. horce_url.pickle 
   - [馬の名前] = 馬のURL
2. race_data.pickle
   - [レースのURL][馬の名前] = []
3. jockey_name.pickle
   - [騎手のURL] = 騎手の名前
4. horce_data_storage.pickle
   - [馬の名前] = レースの文字列リスト
   
### baba_index.py
horce_url.pickleから各レースの馬場指数を収集する。

1. baba_index_data.pickle
   - [馬の名前][生年月日] = 馬場指数
   
### blood_data_get.py
horce_url.pickleからクロスの血統とその割合を収集する。

1. blood_closs_data.pickle
   - [馬の名前] = { "name": 血統のクロスの名前, "rate": 割合(%) }
   
### father_data.py
horce_url.pickleから父親の産駒の情報を取得する。

1. father_name.pickle
   - [馬の名前] = 父親の馬の名前
2. father_grade_data.pickle
   - [馬の名前][年(西暦)] = { "go_num": 出走頭数, "win_num": 勝った馬の数, "win_rate": 勝率, "EI": EI }
3. father_condition_grade.pickle
   - [馬の名前]["kb"]["1400"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["1800"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["2200"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["2600"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["2601"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["1"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["2"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["3"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   - [馬の名前]["kb"]["4"] = { "one": 勝率, "two": 連対率, "three": 複勝率 }
   
### first_time_get.py
race_data.pickleから馬ごとの過去5レースの前半3Fのデータを収集する。

1. first_time.pickle
   - [race_id] = { "name": 馬の名前, "time": 前半3Fのリスト }のリスト
   
### horce_data_collect.py
horce_url.pickleから調教師のURLと性別などの馬の情報を収集する。

1. horce_url.pickle 
   - [馬の名前]["sex"] = 性別
   - [馬の名前]["birth"] = 生まれ年
   - [馬の名前]["trainer"] = 調教師名
   - [馬の名前]["charactor"] = { "course": 芝かダート, "dist": 長いか短い, "foot": 逃げか追い込みか, "growth": 早熟か晩成, "heavy_baba": 重馬場が得意か苦手 }
   
2. trainer_url.pickle
   - [調教師の名前] = 調教師のURL
   
   
